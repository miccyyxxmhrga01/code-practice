import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong Park - W/S, Up/Down, Left/Right, Esc to quit")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

SKY = (135, 206, 235)
SUN = (255, 220, 90)
CLOUD = (250, 250, 250)
HILLS = (105, 180, 100)
GRASS = (80, 160, 75)
SHADOW = (60, 130, 60)
TABLE = (25, 105, 75)
ROAD = (75, 75, 80)
WHITE = (245, 245, 245)
NAVY = (20, 40, 80)
BLACK = (25, 25, 25)
GREY = (170, 170, 170)
BLUE = (70, 130, 230)
ORANGE = (255, 150, 50)
RED = (220, 50, 50)
WINDOW = (170, 220, 255)

HORIZON = 160   # where the sky ends and the grass begins
ROAD_TOP = 480  # where the grass ends and the road begins

# ---------------- Ping-pong ----------------
table = pygame.Rect(110, 195, 680, 260)

PADDLE_SPEED = 7
left_paddle = pygame.Rect(table.left + 15, table.centery - 40, 12, 80)
right_paddle = pygame.Rect(table.right - 27, table.centery - 40, 12, 80)

ball = pygame.Rect(0, 0, 16, 16)
MAX_BALL_SPEED = 12


def serve(direction):
    """Put the ball in the middle of the table and send it left (-1) or right (1)."""
    ball.center = table.center
    return 5 * direction, random.choice([-3, -2, 2, 3])


ball_dx, ball_dy = serve(random.choice([-1, 1]))
wait = 60          # frames to wait before the ball starts moving (60 = 1 second)
left_score = 0
right_score = 0
passes = 0         # how many times the ball was hit in this rally
best_passes = 0

# ---------------- Car ----------------
def make_car(color):
    """Draw a car facing right on its own see-through surface."""
    car = pygame.Surface((120, 60), pygame.SRCALPHA)
    pygame.draw.rect(car, color, (0, 20, 120, 28), border_radius=8)   # body
    pygame.draw.rect(car, color, (25, 2, 62, 26), border_radius=10)   # roof
    pygame.draw.rect(car, WINDOW, (32, 8, 22, 14), border_radius=3)   # back window
    pygame.draw.rect(car, WINDOW, (59, 8, 22, 14), border_radius=3)   # front window
    pygame.draw.circle(car, SUN, (113, 30), 5)                        # headlight
    for wheel_x in (28, 92):
        pygame.draw.circle(car, BLACK, (wheel_x, 46), 13)             # tyre
        pygame.draw.circle(car, GREY, (wheel_x, 46), 5)               # hubcap
    return car


car_image_right = make_car(RED)
car_image_left = pygame.transform.flip(car_image_right, True, False)  # mirror image
CAR_WIDTH = 120
CAR_SPEED = 6
car_x = 100
car_y = ROAD_TOP - 8
facing_right = True
smoke = []         # exhaust puffs: [x, y, radius]

# ---------------- Background ----------------
clouds = [[60, 45, 0.3], [380, 75, 0.5], [640, 40, 0.4]]  # [x, y, speed]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()

    # --- Paddles: W/S moves blue, Up/Down moves orange ---
    if keys[pygame.K_w]:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s]:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP]:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        right_paddle.y += PADDLE_SPEED
    left_paddle.clamp_ip(table)    # keep the paddles on the table
    right_paddle.clamp_ip(table)

    # --- Ball ---
    if wait > 0:
        wait -= 1
    else:
        ball.x += ball_dx
        ball.y += ball_dy

    # Bounce off the long sides of the table
    if ball.top < table.top:
        ball.top = table.top
        ball_dy = abs(ball_dy)
    if ball.bottom > table.bottom:
        ball.bottom = table.bottom
        ball_dy = -abs(ball_dy)

    # A paddle hits it back a little faster.
    # Hitting with the edge of the paddle sends it off at a steeper angle.
    if ball.colliderect(left_paddle) and ball_dx < 0:
        ball_dx = min(-ball_dx + 1, MAX_BALL_SPEED)
        ball_dy = (ball.centery - left_paddle.centery) // 6
        passes += 1
    if ball.colliderect(right_paddle) and ball_dx > 0:
        ball_dx = -min(ball_dx + 1, MAX_BALL_SPEED)
        ball_dy = (ball.centery - right_paddle.centery) // 6
        passes += 1

    # Someone missed: the other player gets a point
    if ball.right < table.left or ball.left > table.right:
        if ball.right < table.left:
            right_score += 1
        else:
            left_score += 1
        best_passes = max(best_passes, passes)
        passes = 0
        wait = 60
        ball_dx, ball_dy = serve(1 if ball_dx > 0 else -1)  # serve to whoever missed

    # --- Car: hold Left/Right to drive ---
    moving = False
    if keys[pygame.K_LEFT]:
        car_x -= CAR_SPEED
        facing_right = False
        moving = True
    if keys[pygame.K_RIGHT]:
        car_x += CAR_SPEED
        facing_right = True
        moving = True

    # Drive off one side of the screen and come back on the other
    if car_x > WIDTH:
        car_x = -CAR_WIDTH
    if car_x < -CAR_WIDTH:
        car_x = WIDTH

    # Puffs of smoke come out of the back of the car while it drives
    if moving:
        back_x = car_x if facing_right else car_x + CAR_WIDTH
        smoke.append([back_x, car_y + 40, 3])
    for puff in smoke[:]:   # loop over a copy because we remove puffs
        puff[1] -= 0.5      # float up
        puff[2] += 0.4      # grow
        if puff[2] > 12:
            smoke.remove(puff)

    # --- Clouds drift slowly to the right ---
    for cloud in clouds:
        cloud[0] += cloud[2]
        if cloud[0] > WIDTH:
            cloud[0] = -100

    # ---------------- Draw everything ----------------
    # Background: sky, sun, clouds, hills, grass, road
    screen.fill(SKY)
    pygame.draw.circle(screen, SUN, (820, 65), 40)
    for x, y, speed in clouds:
        pygame.draw.circle(screen, CLOUD, (x, y), 22)
        pygame.draw.circle(screen, CLOUD, (x + 25, y - 10), 28)
        pygame.draw.circle(screen, CLOUD, (x + 52, y), 22)
    for x, radius in ((90, 60), (280, 80), (500, 55), (720, 75)):
        pygame.draw.circle(screen, HILLS, (x, HORIZON), radius)
    pygame.draw.rect(screen, GRASS, (0, HORIZON, WIDTH, ROAD_TOP - HORIZON))
    pygame.draw.rect(screen, ROAD, (0, ROAD_TOP, WIDTH, HEIGHT - ROAD_TOP))
    for x in range(0, WIDTH, 60):
        pygame.draw.rect(screen, WHITE, (x, 550, 30, 4))  # dashed road line

    # Table with a shadow, white edge, middle line and net
    pygame.draw.rect(screen, SHADOW, table.move(8, 8))
    pygame.draw.rect(screen, TABLE, table)
    pygame.draw.rect(screen, WHITE, table, 4)
    pygame.draw.line(screen, WHITE, (table.left, table.centery), (table.right, table.centery), 2)
    pygame.draw.line(screen, WHITE, (table.centerx, table.top), (table.centerx, table.bottom), 6)

    pygame.draw.rect(screen, BLUE, left_paddle, border_radius=4)
    pygame.draw.rect(screen, ORANGE, right_paddle, border_radius=4)
    pygame.draw.circle(screen, WHITE, ball.center, 8)

    # Car and its smoke
    for x, y, radius in smoke:
        pygame.draw.circle(screen, GREY, (x, y), radius)
    car_image = car_image_right if facing_right else car_image_left
    screen.blit(car_image, (car_x, car_y))

    # Text
    score_text = font.render(f"Blue {left_score}   -   {right_score} Orange", True, NAVY)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 12))
    pass_text = small_font.render(f"Passes: {passes}     Best: {best_passes}", True, NAVY)
    screen.blit(pass_text, (WIDTH // 2 - pass_text.get_width() // 2, 45))
    help_text = small_font.render(
        "W/S: blue paddle     Up/Down: orange paddle     Left/Right: drive the car     Esc: quit",
        True, WHITE)
    screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT - 28))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
