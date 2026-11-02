import math
import random

import pygame


WIDTH, HEIGHT = 800, 560
TOP, BOTTOM = 120, 490
BALL_RADIUS = 9
WINNING_SCORE = 5
WHITE = (235, 241, 250)
BLUE = (100, 195, 255)
ORANGE = (255, 181, 100)


class Pong:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 26)
        self.large_font = pygame.font.Font(None, 44)
        self.player = pygame.Rect(35, 0, 14, 84)
        self.computer = pygame.Rect(WIDTH - 49, 0, 14, 84)
        self.reset()

    def reset(self):
        self.player_score = self.computer_score = 0
        self.player_y = self.computer_y = (TOP + BOTTOM) / 2
        self.player.centery = self.computer.centery = round(self.player_y)
        self.prepare_serve(-1, "Catch the ball with your paddle!")

    def prepare_serve(self, direction, message):
        self.ball = pygame.Vector2(WIDTH / 2, (TOP + BOTTOM) / 2)
        self.velocity = pygame.Vector2()
        self.serve_direction = direction
        self.state = "ready"
        self.message = message

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset()
            elif event.key == pygame.K_SPACE and self.state == "ready":
                self.velocity.update(320 * self.serve_direction, random.choice((-150, 150)))
                self.state = "playing"

    def award_point(self, winner):
        if self.state != "playing":
            return
        if winner == "player":
            self.player_score += 1
            self.prepare_serve(1, "You scored!")
        else:
            self.computer_score += 1
            self.prepare_serve(-1, "Computer scored!")
        if max(self.player_score, self.computer_score) >= WINNING_SCORE:
            self.state = "over"
            self.message = "You win!" if self.player_score >= WINNING_SCORE else "Computer wins!"

    def bounce(self, paddle, direction):
        # Hit near a paddle's edge to send the ball at a sharper angle.
        offset = max(-1, min(1, (self.ball.y - paddle.centery) / (paddle.height / 2)))
        speed = min(580, self.velocity.length() + 25)
        self.velocity.y = offset * speed * 0.8
        self.velocity.x = direction * math.sqrt(speed**2 - self.velocity.y**2)
        edge = paddle.right if direction > 0 else paddle.left
        self.ball.x = edge + direction * BALL_RADIUS

    def update(self, dt, keys):
        if self.state == "over":
            return
        dt = min(dt, 1 / 30)
        direction = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        half_height = self.player.height / 2
        self.player_y = max(TOP + half_height, min(BOTTOM - half_height, self.player_y + direction * 390 * dt))
        self.player.centery = round(self.player_y)

        if self.state != "playing":
            return

        # The computer has a limited speed, so angled shots can beat it.
        target_y = self.ball.y if self.velocity.x > 0 else (TOP + BOTTOM) / 2
        self.computer_y += max(-235 * dt, min(235 * dt, target_y - self.computer_y))
        self.computer_y = max(TOP + half_height, min(BOTTOM - half_height, self.computer_y))
        self.computer.centery = round(self.computer_y)

        self.ball += self.velocity * dt
        if self.ball.y - BALL_RADIUS <= TOP:
            self.ball.y = TOP + BALL_RADIUS
            self.velocity.y = abs(self.velocity.y)
        elif self.ball.y + BALL_RADIUS >= BOTTOM:
            self.ball.y = BOTTOM - BALL_RADIUS
            self.velocity.y = -abs(self.velocity.y)

        ball_rect = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball_rect.center = (round(self.ball.x), round(self.ball.y))
        if self.velocity.x < 0 and ball_rect.colliderect(self.player):
            self.bounce(self.player, 1)
        elif self.velocity.x > 0 and ball_rect.colliderect(self.computer):
            self.bounce(self.computer, -1)

        if self.ball.x + BALL_RADIUS < 0:
            self.award_point("computer")
        elif self.ball.x - BALL_RADIUS > WIDTH:
            self.award_point("player")

    def text(self, label, center, color=WHITE, large=False):
        font = self.large_font if large else self.font
        surface = font.render(label, True, color)
        self.screen.blit(surface, surface.get_rect(center=center))

    def draw(self):
        self.screen.fill((20, 29, 45))
        self.text("CATCH & BOUNCE", (WIDTH // 2, 32), large=True)
        self.text(f"YOU  {self.player_score}", (180, 83), BLUE, large=True)
        self.text(f"COMPUTER  {self.computer_score}", (610, 83), ORANGE, large=True)
        self.text(f"First to {WINNING_SCORE}", (WIDTH // 2, 83))

        pygame.draw.rect(self.screen, (26, 40, 59), (20, TOP, WIDTH - 40, BOTTOM - TOP))
        for y in range(TOP + 8, BOTTOM, 24):
            pygame.draw.line(self.screen, (61, 80, 101), (WIDTH // 2, y), (WIDTH // 2, min(y + 12, BOTTOM)), 3)
        for y in (TOP, BOTTOM):
            pygame.draw.line(self.screen, (93, 114, 134), (20, y), (WIDTH - 20, y), 2)
        pygame.draw.rect(self.screen, BLUE, self.player, border_radius=6)
        pygame.draw.rect(self.screen, ORANGE, self.computer, border_radius=6)
        pygame.draw.circle(self.screen, WHITE, (round(self.ball.x), round(self.ball.y)), BALL_RADIUS)

        if self.state == "ready":
            self.text(self.message, (WIDTH // 2, 205), (255, 221, 110))
            self.text("Press SPACE to serve", (WIDTH // 2, 238))
        elif self.state == "over":
            pygame.draw.rect(self.screen, (20, 29, 45), (180, 205, 440, 145), border_radius=12)
            self.text(self.message, (WIDTH // 2, 252), (255, 221, 110), large=True)
            self.text("Press R to play again", (WIDTH // 2, 304))
        self.text("UP/DOWN or W/S: Move    SPACE: Serve    R: Restart    ESC: Quit", (WIDTH // 2, 530))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch & Bounce - Simple Pong")
    clock = pygame.time.Clock()
    game = Pong(screen)
    running = True
    try:
        while running:
            dt = clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                else:
                    game.handle_event(event)
            game.update(dt, pygame.key.get_pressed())
            game.draw()
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
