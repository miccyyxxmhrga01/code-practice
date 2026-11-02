import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch! - left/right arrows to move, Esc to quit")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

BACKGROUND = (30, 30, 40)
WHITE = (245, 245, 245)
BLUE = (70, 130, 230)
YELLOW = (255, 220, 90)

# The basket is a rectangle near the bottom of the screen
basket = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 20)
BASKET_SPEED = 10


def make_ball():
    """A new ball just above the top of the screen, at a random x."""
    x = random.randint(20, WIDTH - 40)
    return pygame.Rect(x, -20, 20, 20)


balls = []
spawn_timer = 0  # counts frames until the next ball appears
score = 0
lives = 3

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and lives == 0:
                # Play again
                balls = []
                score = 0
                lives = 3

    if lives > 0:
        # Hold the arrow keys to move the basket, and keep it on the screen.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.x -= BASKET_SPEED
        if keys[pygame.K_RIGHT]:
            basket.x += BASKET_SPEED
        basket.x = max(0, min(WIDTH - basket.width, basket.x))

        # A new ball every 60 frames (= 1 second)
        spawn_timer += 1
        if spawn_timer >= 60:
            balls.append(make_ball())
            spawn_timer = 0

        # Balls fall faster as the score goes up
        fall_speed = 4 + score // 5

        # Loop over a copy (balls[:]) because we remove balls while looping
        for ball in balls[:]:
            ball.y += fall_speed
            if ball.colliderect(basket):  # the two rectangles overlap
                balls.remove(ball)
                score += 1
            elif ball.top > HEIGHT:       # fell past the bottom
                balls.remove(ball)
                lives -= 1

    # Draw everything
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, BLUE, basket)
    for ball in balls:
        pygame.draw.circle(screen, YELLOW, ball.center, 10)

    screen.blit(font.render(f"Score: {score}   Lives: {lives}", True, WHITE), (10, 10))
    if lives == 0:
        message = font.render("GAME OVER - press Space to play again", True, WHITE)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
