"""Simple badminton: A/D or arrows to move, Space to serve/swing, R to reset."""

import math
import random

import pygame


WIDTH, HEIGHT = 900, 600
FLOOR = 510
NET_X, NET_TOP = WIDTH // 2, 335
GRAVITY = 800
WINNING_SCORE = 5
WHITE = (240, 246, 244)


class Badminton:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.reset()

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.prepare_serve("Move under the shuttle and swing!")

    def prepare_serve(self, message):
        self.player_x = 180.0
        self.computer_x = 720.0
        self.shuttle = pygame.Vector2(self.player_x + 36, FLOOR - 130)
        self.velocity = pygame.Vector2()
        self.last_hitter = "player"
        self.swing_timer = 0
        self.swing_cooldown = 0
        self.computer_swing = 0
        self.state = "ready"
        self.message = message

    def hit(self, hitter):
        # Aim an upward arc at a safe spot on the opposite court.
        target_x = random.uniform(560, 820) if hitter == "player" else random.uniform(80, 340)
        self.velocity.y = -540
        flight_time = (540 + math.sqrt(540**2 + 2 * GRAVITY * (FLOOR - 6 - self.shuttle.y))) / GRAVITY
        self.velocity.x = (target_x - self.shuttle.x) / flight_time
        self.last_hitter = hitter

    def award_point(self, winner):
        if self.state != "playing":
            return
        if winner == "player":
            self.player_score += 1
            message = "You scored!"
        else:
            self.computer_score += 1
            message = "Computer scored!"

        self.prepare_serve(message)
        if max(self.player_score, self.computer_score) >= WINNING_SCORE:
            self.state = "over"
            self.message = "You win!" if self.player_score >= WINNING_SCORE else "Computer wins!"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_r:
            self.reset()
        elif event.key == pygame.K_SPACE:
            if self.state == "ready":
                self.state = "playing"
                self.hit("player")
            elif self.state == "playing" and self.swing_cooldown <= 0:
                self.swing_timer = 0.22
                self.swing_cooldown = 0.35

    def update(self, dt, keys):
        if self.state == "over":
            return

        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player_x = max(40, min(NET_X - 80, self.player_x + direction * 320 * dt))
        self.swing_timer = max(0, self.swing_timer - dt)
        self.swing_cooldown = max(0, self.swing_cooldown - dt)
        self.computer_swing = max(0, self.computer_swing - dt)

        if self.state == "ready":
            self.shuttle.update(self.player_x + 36, FLOOR - 130)
            return

        # The computer follows the shuttle on its own half of the court.
        target = self.shuttle.x + 36 if self.shuttle.x > NET_X else 720
        target = max(NET_X + 80, min(WIDTH - 40, target))
        self.computer_x += max(-210 * dt, min(210 * dt, target - self.computer_x))

        previous_x = self.shuttle.x
        self.shuttle += self.velocity * dt + pygame.Vector2(0, 0.5 * GRAVITY * dt * dt)
        self.velocity.y += GRAVITY * dt

        # Net faults and out-of-bounds shots give the other side a point.
        crossed_net = (previous_x - NET_X) * (self.shuttle.x - NET_X) <= 0
        touching_net = abs(self.shuttle.x - NET_X) <= 9 or crossed_net
        if touching_net and self.shuttle.y + 6 >= NET_TOP:
            self.award_point("computer" if self.last_hitter == "player" else "player")
            return
        if self.shuttle.x < 0 or self.shuttle.x > WIDTH:
            self.award_point("computer" if self.last_hitter == "player" else "player")
            return
        if self.shuttle.y + 6 >= FLOOR:
            self.award_point("computer" if self.shuttle.x < NET_X else "player")
            return

        player_racket = pygame.Vector2(self.player_x + 36, FLOOR - 100)
        computer_racket = pygame.Vector2(self.computer_x - 36, FLOOR - 100)
        if (self.swing_timer > 0 and self.last_hitter == "computer"
                and self.shuttle.x < NET_X and self.shuttle.distance_to(player_racket) < 76):
            self.hit("player")
            self.swing_timer = 0  # Each swing can hit only once.
        elif (self.last_hitter == "player" and self.shuttle.x > NET_X
                and self.velocity.y > 0 and self.shuttle.distance_to(computer_racket) < 65):
            self.hit("computer")
            self.computer_swing = 0.2

    def text(self, label, position, color=WHITE, big=False):
        font = self.big_font if big else self.font
        surface = font.render(label, True, color)
        self.screen.blit(surface, surface.get_rect(center=position))

    def draw_player(self, x, color, facing, swinging):
        x = int(x)
        pygame.draw.ellipse(self.screen, (26, 76, 63), (x - 29, FLOOR - 5, 58, 12))
        pygame.draw.circle(self.screen, (245, 206, 162), (x, FLOOR - 85), 14)
        pygame.draw.rect(self.screen, color, (x - 17, FLOOR - 68, 34, 40), border_radius=8)
        pygame.draw.line(self.screen, WHITE, (x - 9, FLOOR - 29), (x - 16, FLOOR), 7)
        pygame.draw.line(self.screen, WHITE, (x + 9, FLOOR - 29), (x + 16, FLOOR), 7)
        racket_x, racket_y = x + facing * 36, FLOOR - 100
        pygame.draw.line(self.screen, (245, 206, 162), (x, FLOOR - 55), (racket_x, racket_y + 26), 6)
        pygame.draw.line(self.screen, WHITE, (racket_x, racket_y + 26), (racket_x, racket_y + 14), 4)
        racket_color = (255, 224, 105) if swinging else WHITE
        pygame.draw.ellipse(self.screen, racket_color, (racket_x - 13, racket_y - 20, 26, 40), 3)
        pygame.draw.line(self.screen, racket_color, (racket_x - 10, racket_y), (racket_x + 10, racket_y), 1)
        pygame.draw.line(self.screen, racket_color, (racket_x, racket_y - 16), (racket_x, racket_y + 16), 1)
        if swinging:
            pygame.draw.arc(self.screen, racket_color, (racket_x - 37, racket_y - 42, 74, 84), -1.2, 1.2, 3)

    def draw(self):
        self.screen.fill((19, 43, 49))
        pygame.draw.rect(self.screen, (40, 115, 89), (20, 175, WIDTH - 40, FLOOR - 155), border_radius=16)
        pygame.draw.line(self.screen, (105, 172, 136), (45, FLOOR), (WIDTH - 45, FLOOR), 3)
        pygame.draw.line(self.screen, (105, 172, 136), (100, FLOOR + 18), (WIDTH - 100, FLOOR + 18), 2)

        self.text("BADMINTON", (WIDTH // 2, 34), big=True)
        self.text(f"YOU  {self.player_score}", (210, 94), (114, 211, 255), big=True)
        self.text(f"CPU  {self.computer_score}", (690, 94), (255, 181, 112), big=True)
        self.text(f"First to {WINNING_SCORE}", (WIDTH // 2, 95))

        # A narrow side view of the net.
        for y in range(NET_TOP, FLOOR, 14):
            pygame.draw.line(self.screen, (182, 207, 195), (NET_X - 9, y), (NET_X + 9, y), 1)
        for x in (NET_X - 9, NET_X, NET_X + 9):
            pygame.draw.line(self.screen, (182, 207, 195), (x, NET_TOP), (x, FLOOR), 2)
        pygame.draw.line(self.screen, WHITE, (NET_X - 12, NET_TOP), (NET_X + 12, NET_TOP), 5)

        self.draw_player(self.player_x, (65, 174, 238), 1, self.swing_timer > 0)
        self.draw_player(self.computer_x, (240, 147, 77), -1, self.computer_swing > 0)

        if self.state != "over":
            # Feather tail and round cork: no image files needed.
            tip = self.shuttle
            tail = -self.velocity.normalize() if self.velocity.length_squared() else pygame.Vector2(-1, -1).normalize()
            side = pygame.Vector2(-tail.y, tail.x)
            pygame.draw.polygon(self.screen, WHITE, [tip, tip + tail * 20 + side * 9, tip + tail * 20 - side * 9])
            pygame.draw.circle(self.screen, (255, 221, 111), (round(tip.x), round(tip.y)), 6)

        if self.state == "ready":
            self.text(self.message + "  Press SPACE to serve.", (WIDTH // 2, 148), (255, 224, 105))
        elif self.state == "over":
            panel = pygame.Rect(170, 205, 560, 105)
            pygame.draw.rect(self.screen, (19, 43, 49), panel, border_radius=12)
            self.text(self.message, (WIDTH // 2, 242), (255, 224, 105), big=True)
            self.text("Press R to play again", (WIDTH // 2, 283))
        else:
            self.text("Get close to the shuttle, then press SPACE!", (WIDTH // 2, 148))
        self.text("A/D or arrows: Move     SPACE: Serve / Swing     R: Restart     ESC: Quit", (WIDTH // 2, 565))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Badminton")
    clock = pygame.time.Clock()
    game = Badminton(screen)
    running = True

    try:
        while running:
            dt = min(clock.tick(60) / 1000, 1 / 30)
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
