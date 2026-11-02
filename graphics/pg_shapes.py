import pygame

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Shapes - Esc to quit")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

BACKGROUND = (30, 30, 40)
WHITE = (245, 245, 245)
RED = (220, 50, 50)
GREEN = (80, 200, 120)
BLUE = (70, 130, 230)
YELLOW = (255, 220, 90)
PURPLE = (170, 90, 220)


def draw_label(text, x, y):
    """Write text centred on x."""
    image = font.render(text, True, WHITE)
    screen.blit(image, (x - image.get_width() // 2, y))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BACKGROUND)

    # Top row: filled shapes
    pygame.draw.rect(screen, RED, (70, 80, 120, 120))
    draw_label("rect", 130, 215)

    pygame.draw.circle(screen, GREEN, (320, 140), 60)
    draw_label("circle", 320, 215)

    pygame.draw.ellipse(screen, BLUE, (420, 100, 160, 80))
    draw_label("ellipse", 500, 215)

    pygame.draw.polygon(screen, YELLOW, [(690, 80), (750, 200), (630, 200)])
    draw_label("polygon", 690, 215)

    # Bottom row: outlines and lines (the last number is the line width)
    pygame.draw.rect(screen, RED, (70, 290, 120, 120), 4)
    draw_label("rect outline", 130, 425)

    pygame.draw.circle(screen, GREEN, (320, 350), 60, 4)
    draw_label("circle outline", 320, 425)

    pygame.draw.line(screen, PURPLE, (430, 300), (570, 400), 5)
    draw_label("line", 500, 425)

    zigzag = [(630, 400), (660, 300), (690, 380), (720, 300), (750, 400)]
    pygame.draw.lines(screen, YELLOW, False, zigzag, 4)
    draw_label("lines", 690, 425)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
