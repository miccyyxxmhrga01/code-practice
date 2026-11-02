import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Paddle dimensions
paddle_width = 10
paddle_height = 80

# Paddle speed
paddle_speed = 5

# Ball dimensions
ball_size = 20

# Paddle positions
paddle1_pos = (20, (screen_height - paddle_height) // 2)
paddle2_pos = (screen_width - 20 - paddle_width, (screen_height - paddle_height) // 2)

# Ball position and velocity
ball_pos = (screen_width // 2, screen_height // 2)
ball_velocity = (1, 1)  # Initial velocity (x, y)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and paddle1_pos[1] > 0:
        paddle1_pos = (paddle1_pos[0], paddle1_pos[1] - paddle_speed)
    if key[pygame.K_s] and paddle1_pos[1] < screen_height - paddle_height:
        paddle1_pos = (paddle1_pos[0], paddle1_pos[1] + paddle_speed)

    if key[pygame.K_UP] and paddle2_pos[1] > 0:
        paddle2_pos = (paddle2_pos[0], paddle2_pos[1] - paddle_speed)
    if key[pygame.K_DOWN] and paddle2_pos[1] < screen_height - paddle_height:
        paddle2_pos = (paddle2_pos[0], paddle2_pos[1] + paddle_speed)

    # Ball movement
    ball_pos = (ball_pos[0] + ball_velocity[0], ball_pos[1] + ball_velocity[1])

    # Ball collisions with walls
    if ball_pos[0] <= 0 or ball_pos[0] >= screen_width - ball_size:
        ball_velocity[0] = -ball_velocity[0]  # Reverse x velocity

    if ball_pos[1] <= 0 or ball_pos[1] >= screen_height - ball_size:
        ball_velocity[1] = -ball_velocity[1]  # Reverse y velocity

    # Ball collisions with paddles
    if (paddle1_pos[0] <= ball_pos[0] <= paddle1_pos[0] + paddle_width and
        paddle1_pos[1] <= ball_pos[1] <= paddle1_pos[1] + paddle_height):
        ball_velocity[0] = -ball_velocity[0]

    if (paddle2_pos[0] <= ball_pos[0] <= paddle2_pos[0] + paddle_width and
        paddle2_pos[1] <= ball_pos[1] <= paddle2_pos[1] + paddle_height):
        ball_velocity[0] = -ball_velocity[0]

    # Drawing
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill(black)

    # Draw paddles
    pygame.draw.rect(screen, white, (paddle1_pos[0], paddle1_pos[1], paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (paddle2_pos[0], paddle2_pos[1], paddle_width, paddle_height))

    # Draw ball
    pygame.draw.circle(screen, red, ball_pos, ball_size)

    # Update display
    pygame.display.update()

    # Control game speed
    pygame.time.delay(30)

pygame.quit()