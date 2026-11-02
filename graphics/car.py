import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hill Car")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

SKY = (135, 206, 235)
GROUND = (74, 160, 70)
FAR_HILLS = (120, 185, 110)
ROAD = (90, 90, 90)
BLACK = (20, 20, 20)
RED = (220, 50, 50)
WHITE = (245, 245, 245)
GREY = (160, 160, 160)
SUN = (255, 220, 90)
WINDOW = (170, 220, 255)

WHEEL_RADIUS = 14
WHEEL_GAP = 30 
ROAD_Y = 450
ROAD_HEIGHT = 60

speed = 4
scroll = 0     
wheel_spin = 0

car_x = 380

clouds = [[random.randint(0, WIDTH), random.randint(40, 200), random.randint(25, 45)] for _ in range(6)]


def draw_background():
    screen.fill(SKY)
    pygame.draw.circle(screen, SUN, (780, 90), 45)

    for x, y, size in clouds:
        cx = (x - scroll * 0.2) % (WIDTH + 200) - 100
        pygame.draw.circle(screen, WHITE, (cx, y), size)
        pygame.draw.circle(screen, WHITE, (cx - size * 0.8, y + size * 0.3), size * 0.7)
        pygame.draw.circle(screen, WHITE, (cx + size * 0.8, y + size * 0.3), size * 0.7)

    far = [(sx, 340 + 50 * math.sin((sx + scroll * 0.4) * 0.006)) for sx in range(0, WIDTH + 10, 10)]
    pygame.draw.polygon(screen, FAR_HILLS, [(0, HEIGHT)] + far + [(WIDTH, HEIGHT)])


def draw_road():
    pygame.draw.rect(screen, GROUND, (0, ROAD_Y - 30, WIDTH, HEIGHT))
    pygame.draw.rect(screen, ROAD, (0, ROAD_Y, WIDTH, ROAD_HEIGHT))

    dash_y = ROAD_Y + ROAD_HEIGHT // 2 - 2
    for x in range(-int(scroll) % 80 - 80, WIDTH, 80):
        pygame.draw.rect(screen, WHITE, (x, dash_y, 40, 4))


def draw_car():
    wheel_y = ROAD_Y + 10 - WHEEL_RADIUS
    back = pygame.Vector2(car_x - WHEEL_GAP, wheel_y)
    front = pygame.Vector2(car_x + WHEEL_GAP, wheel_y)

    def place(points):
        return [(car_x + x, wheel_y + y) for x, y in points]

    body = [(-50, 4), (50, 4), (50, -14), (40, -22), (18, -24), (6, -42),
            (-26, -42), (-38, -24), (-50, -20)]
    front_window = [(-8, -26), (-8, -38), (5, -38), (13, -26)]
    back_window = [(-12, -26), (-12, -38), (-23, -38), (-32, -26)]

    pygame.draw.polygon(screen, RED, place(body))
    pygame.draw.polygon(screen, WINDOW, place(front_window))
    pygame.draw.polygon(screen, WINDOW, place(back_window))
    pygame.draw.circle(screen, SUN, place([(46, -10)])[0], 4)

    for wheel in (back, front):
        pygame.draw.circle(screen, BLACK, wheel, WHEEL_RADIUS)
        pygame.draw.circle(screen, GREY, wheel, 5)
        for i in range(3):
            spoke = pygame.Vector2(WHEEL_RADIUS - 3, 0).rotate_rad(wheel_spin + i * math.pi / 3)
            pygame.draw.line(screen, GREY, wheel - spoke, wheel + spoke, 2)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move = 0
    if keys[pygame.K_RIGHT]:
        move += speed
    if keys[pygame.K_LEFT]:
        move -= speed
    scroll += move
    wheel_spin += move / WHEEL_RADIUS

    draw_background()
    draw_road()
    draw_car()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
