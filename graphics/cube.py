
import math
import sys

import pygame

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Camera Movement and Rotation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)  # make the font once, not every frame

# A cube from -1 to 1. Each face's corners go around in order, so the edges join up
BASE_VERTICES = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # back face
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),      # front face
]
EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # back face
    (4, 5), (5, 6), (6, 7), (7, 4),  # front face
    (0, 4), (1, 5), (2, 6), (3, 7),  # joining the two faces
]

camera_pos = [0.0, 0.0, -5.0]  # x, y, z: starts 5 units in front of the cube
camera_rot = [0.0, 0.0]        # pitch (look up/down), yaw (turn left/right), in radians
camera_rot_z = 0.0             # roll (tilt), in radians
cube_scale = 1.0

MOVE_SPEED = 3.0   # units per second
TURN_SPEED = 1.5   # radians per second
FOCAL = 400        # bigger = more zoomed in


def rotate_point(x, y, z, pitch, yaw, roll):
    """Turn a point around the y axis (yaw), then the x axis (pitch), then the z axis (roll)."""
    c, s = math.cos(yaw), math.sin(yaw)
    x, z = x * c - z * s, x * s + z * c
    c, s = math.cos(pitch), math.sin(pitch)
    y, z = y * c - z * s, y * s + z * c
    c, s = math.cos(roll), math.sin(roll)
    x, y = x * c - y * s, x * s + y * c
    return x, y, z


def to_camera(vertex):
    """A cube corner as the camera sees it: scaled, moved, then turned the opposite way."""
    x, y, z = (v * cube_scale for v in vertex)
    x -= camera_pos[0]
    y -= camera_pos[1]
    z -= camera_pos[2]
    return rotate_point(x, y, z, -camera_rot[0], -camera_rot[1], -camera_rot_z)


def project(x, y, z):
    """Camera space to a screen position, or None if the point is behind the camera."""
    if z <= 0.1:
        return None
    f = FOCAL / z
    return WIDTH / 2 + x * f, HEIGHT / 2 - y * f


def draw_cube():
    # The closer the camera, the brighter the cube
    distance = math.sqrt(sum(c * c for c in camera_pos))
    intensity = max(50, min(255, int(255 - distance * 20)))
    color = (0, intensity, intensity)

    points = [project(*to_camera(v)) for v in BASE_VERTICES]
    for a, b in EDGES:
        if points[a] and points[b]:  # skip edges that go behind the camera
            pygame.draw.line(screen, color, points[a], points[b], 2)
    for p in points:
        if p:
            pygame.draw.circle(screen, (255, 255, 255), (round(p[0]), round(p[1])), 4)


def move_camera(keys, dt):
    global camera_rot_z, cube_scale
    # Turning: arrow keys look around, Q/E tilt
    camera_rot[1] += (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * TURN_SPEED * dt
    camera_rot[0] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * TURN_SPEED * dt
    camera_rot[0] = max(-1.5, min(1.5, camera_rot[0]))  # don't flip over the top
    camera_rot_z += (keys[pygame.K_q] - keys[pygame.K_e]) * TURN_SPEED * dt

    # Moving: W/S forward and back, A/D sideways, R/F up and down (relative to where you face)
    yaw = camera_rot[1]
    forward = (-math.sin(yaw), 0.0, math.cos(yaw))
    right = (math.cos(yaw), 0.0, math.sin(yaw))
    step = MOVE_SPEED * dt
    ahead = keys[pygame.K_w] - keys[pygame.K_s]
    side = keys[pygame.K_d] - keys[pygame.K_a]
    for i in range(3):
        camera_pos[i] += (forward[i] * ahead + right[i] * side) * step
    camera_pos[1] += (keys[pygame.K_r] - keys[pygame.K_f]) * step

    # Size: + and - (also on the number pad)
    if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
        cube_scale = min(5.0, cube_scale * (1 + dt))
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        cube_scale = max(0.2, cube_scale * (1 - dt))


running = True
while running:
    dt = clock.tick(60) / 1000  # seconds since the last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    move_camera(pygame.key.get_pressed(), dt)

    screen.fill((15, 15, 25))  # dark, so the white text shows
    draw_cube()

    pos = ", ".join(f"{c:.1f}" for c in camera_pos)
    rot = ", ".join(f"{math.degrees(r):.0f}" for r in camera_rot)
    info = f"Pos: ({pos})  Rot: ({rot})  Roll: {math.degrees(camera_rot_z):.0f}  Scale: {cube_scale:.2f}"
    screen.blit(font.render(info, True, (255, 255, 255)), (20, 20))
    help_text = "WASD move, R/F up/down, arrows look, Q/E roll, +/- size, Esc quit"
    screen.blit(font.render(help_text, True, (150, 150, 170)), (20, HEIGHT - 35))
    pygame.display.flip()

pygame.quit()
sys.exit()