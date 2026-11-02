import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls - click to add a ball, Esc to quit")
clock = pygame.time.Clock()

GRAVITY = 0.4   # added to the downward speed every frame
BOUNCE = 0.85   # how much speed a ball keeps after hitting the floor


def make_ball(x, y):
    return {
        "x": x,
        "y": y,
        "vx": random.uniform(-5, 5),
        "vy": random.uniform(-8, 0),
        "r": random.randint(12, 30),
        "color": (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)),
    }


balls = [make_ball(random.randint(50, WIDTH - 50), random.randint(50, 200)) for _ in range(5)]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(make_ball(*event.pos))

    for b in balls:
        b["vy"] += GRAVITY
        b["x"] += b["vx"]
        b["y"] += b["vy"]

        # Bounce off the side walls
        if b["x"] - b["r"] < 0 or b["x"] + b["r"] > WIDTH:
            b["vx"] = -b["vx"]
            b["x"] = max(b["r"], min(WIDTH - b["r"], b["x"]))

        # Bounce off the ceiling
        if b["y"] - b["r"] < 0:
            b["y"] = b["r"]
            b["vy"] = -b["vy"]

        # Bounce off the floor, losing a little speed each time
        if b["y"] + b["r"] > HEIGHT:
            b["y"] = HEIGHT - b["r"]
            b["vy"] = -b["vy"] * BOUNCE
            b["vx"] *= 0.99  # a little friction so balls slowly stop rolling

    screen.fill((30, 30, 40))
    for b in balls:
        pygame.draw.circle(screen, b["color"], (b["x"], b["y"]), b["r"])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
