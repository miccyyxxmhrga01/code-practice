import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Move the square! Arrow keys to move, Esc to quit")
    clock = pygame.time.Clock()

    player = pygame.Rect(300, 220, 40, 40)
    speed = 5
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Hold the arrow keys to move the square.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed

        # Keep the square inside the window.
        player.clamp_ip(screen.get_rect())

        screen.fill((30, 30, 40))
        pygame.draw.rect(screen, (80, 200, 120), player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
