import pygame
from vpython import *

# 3D view (VPython): opens in your browser
scene = canvas(title="3D View", width=700, height=450,
               background=color.gray(0.2))
scene.caption = "Click the pygame window, then use the arrow keys to move the ball."

# A 10 x 10 floor with a ball on it
box(pos=vector(0, -0.1, 0), size=vector(10, 0.2, 10), color=color.green)
ball = sphere(pos=vector(0, 0.5, 0), radius=0.5, color=color.red)

# Camera above and in front of the floor, looking at the middle
scene.camera.pos = vector(0, 8, 12)
scene.camera.axis = vector(0, -8, -12)

# 2D view (pygame): the same floor seen from straight above
pygame.init()
SIZE = 400
SCALE = SIZE / 10  # pixels per 3D unit (the floor is 10 units wide)
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Top View - arrow keys to move, Esc to quit")

x, z = 0.0, 0.0  # ball position on the floor
speed = 0.1
running = True

while running:
    rate(60)  # keeps both views at 60 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hold the arrow keys to move the ball.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        z -= speed
    if keys[pygame.K_DOWN]:
        z += speed

    # Keep the ball on the floor.
    x = max(-4.5, min(4.5, x))
    z = max(-4.5, min(4.5, z))

    # Update the 3D view
    ball.pos = vector(x, 0.5, z)

    # Update the 2D view: 3D (x, z) becomes screen (x, y)
    screen.fill((40, 140, 60))
    center = (SIZE / 2 + x * SCALE, SIZE / 2 + z * SCALE)
    pygame.draw.circle(screen, (220, 50, 50), center, 0.5 * SCALE)
    pygame.display.flip()

pygame.quit()
print("Pygame window closed. Close the browser tab or press Ctrl+C to stop.")
