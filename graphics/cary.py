import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Car - Hold Left/Right to move, Esc to quit")
clock = pygame.time.Clock()

SKY = (135, 206, 235)
SUN = (255, 220, 90)
CLOUD = (255, 255, 255)
MOUNTAIN = (120, 185, 110)
GRASS = (74, 160, 70)
TRUNK = (120, 75, 40)
LEAVES = (35, 120, 50)
ROAD = (90, 90, 90)
RED = (220, 50, 50)
WINDOW = (170, 220, 255)
BLACK = (20, 20, 20)

car_x = 100
car_y = 100
speed = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    if not running:
        break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= speed
    if keys[pygame.K_RIGHT]:
        car_x += speed
    if keys[pygame.K_UP]:
        car_y += speed
    if keys[pygame.K_DOWN]:
        car_y+= speed

    if car_x > WIDTH:
        car_x = -100
    elif car_x < -100:
        car_x = WIDTH

    screen.fill(SKY)
    pygame.draw.circle(screen, SUN, (780, 90), 45)

    
    for cloud_x, cloud_y in [(130, 100), (370, 155), (590, 80)]:
        pygame.draw.circle(screen, CLOUD, (cloud_x - 35, cloud_y), 28)
        pygame.draw.circle(screen, CLOUD, (cloud_x, cloud_y - 15), 38)
        pygame.draw.circle(screen, CLOUD, (cloud_x + 35, cloud_y), 28)

    
    pygame.draw.polygon(screen, MOUNTAIN, [(0, 420), (150, 240), (300, 420)])
    pygame.draw.polygon(screen, MOUNTAIN, [(250, 420), (450, 200), (650, 420)])
    pygame.draw.polygon(screen, MOUNTAIN, [(600, 420), (750, 240), (900, 420)])
    pygame.draw.rect(screen, GRASS, (0, 420, WIDTH, 180))

  
    for tree_x in [65, 300, 580, 830]:
        pygame.draw.rect(screen, TRUNK, (tree_x - 10, 380, 20, 45))
        pygame.draw.polygon(screen, LEAVES, [
            (tree_x - 40, 390), (tree_x, 315), (tree_x + 40, 390)
        ])

    pygame.draw.rect(screen, ROAD, (0, 430, WIDTH, 110))
    for lane_x in range(0, WIDTH, 100):
        pygame.draw.rect(screen, (255, 255, 255), (lane_x, 495, 55, 5))

    pygame.draw.rect(screen, RED, (car_x, 410, 100, 30))
    pygame.draw.rect(screen, RED, (car_x + 20, 385, 60, 25))
    pygame.draw.rect(screen, WINDOW, (car_x + 28, 390, 20, 16))
    pygame.draw.rect(screen, WINDOW, (car_x + 52, 390, 20, 16))
    pygame.draw.circle(screen, BLACK, (car_x + 22, 446), 14)
    pygame.draw.circle(screen, BLACK, (car_x + 78, 446), 14)
    pygame.draw.circle(screen, (180, 180, 180), (car_x + 22, 446), 6)
    pygame.draw.circle(screen, (180, 180, 180), (car_x + 78, 446), 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
