import pygame

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

BACKGROUND = (245, 245, 245)
COLORS = {
    pygame.K_1: (20, 20, 20),     # black
    pygame.K_2: (220, 50, 50),    # red
    pygame.K_3: (80, 200, 120),   # green
    pygame.K_4: (70, 130, 230),   # blue
    pygame.K_5: (255, 200, 40),   # yellow
}

# Paint on a separate surface so the help text never gets painted over.
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BACKGROUND)

brush_color = COLORS[pygame.K_1]
brush_size = 6
last_pos = None  # where the mouse was last frame while drawing

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in COLORS:
                brush_color = COLORS[event.key]
            elif event.key == pygame.K_c:
                canvas.fill(BACKGROUND)
            elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                brush_size = min(40, brush_size + 2)
            elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                brush_size = max(2, brush_size - 2)

    # Hold the left mouse button to draw. Joining last frame's point to this
    # one with a line keeps the stroke smooth when the mouse moves fast.
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if last_pos:
            pygame.draw.line(canvas, brush_color, last_pos, pos, brush_size)
        pygame.draw.circle(canvas, brush_color, pos, brush_size // 2)
        last_pos = pos
    else:
        last_pos = None

    screen.blit(canvas, (0, 0))
    help_text = f"Drag to draw | 1-5 color | +/- size ({brush_size}) | C clear | Esc quit"
    screen.blit(font.render(help_text, True, (120, 120, 120)), (10, HEIGHT - 25))
    pygame.draw.circle(screen, brush_color, (WIDTH - 25, HEIGHT - 17), 10)  # current color
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
