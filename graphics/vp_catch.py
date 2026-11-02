from vpython import *
import random

scene = canvas(title="Catch! in 3D", width=800, height=500,
               background=color.gray(0.2))
scene.caption = "Click the 3D view first. Left/right arrows move the basket. Space plays again."

# Floor with its top at y = 0, and a basket sitting on it
box(pos=vector(0, -0.1, 0), size=vector(12, 0.2, 3), color=color.green)
basket = box(pos=vector(0, 0.25, 0), size=vector(2, 0.5, 2), color=color.blue)

# Text that floats in the 3D scene
score_label = label(pos=vector(0, 10, 0), text="", box=False, height=20)

# Camera in front and a little above, looking at the middle of the play area
scene.camera.pos = vector(0, 6, 12)
scene.camera.axis = vector(0, -1.5, -12)

BASKET_SPEED = 8  # units per second
dt = 1 / 60       # one frame at rate(60)


def make_ball():
    """A new ball high above the floor, at a random x."""
    x = random.uniform(-5, 5)
    return sphere(pos=vector(x, 9, 0), radius=0.3, color=color.yellow)


balls = []
spawn_timer = 0  # counts frames until the next ball appears
score = 0
lives = 3

while True:
    rate(60)
    keys = keysdown()  # the keys being held down right now

    if lives == 0:
        score_label.text = f"Score: {score}   GAME OVER - press Space"
        if ' ' in keys:
            # Play again. VPython can't delete objects, so we hide the old balls.
            for ball in balls:
                ball.visible = False
            balls = []
            score = 0
            lives = 3
        continue

    # Hold the arrow keys to move the basket, and keep it on the floor.
    x = basket.pos.x
    if 'left' in keys:
        x -= BASKET_SPEED * dt
    if 'right' in keys:
        x += BASKET_SPEED * dt
    x = max(-5, min(5, x))
    basket.pos = vector(x, 0.25, 0)

    # A new ball every 60 frames (= 1 second)
    spawn_timer += 1
    if spawn_timer >= 60:
        balls.append(make_ball())
        spawn_timer = 0

    # Balls fall faster as the score goes up
    fall_speed = 3 + score / 5  # units per second

    # Loop over a copy (balls[:]) because we remove balls while looping
    for ball in balls[:]:
        ball.pos = ball.pos - vector(0, fall_speed * dt, 0)

        # Caught: the ball reached the top of the basket (y = 0.5)
        # and is above it (basket is 2 wide, so 1 each side of its centre,
        # plus a little extra for the ball's own size)
        if ball.pos.y - ball.radius < 0.5 and abs(ball.pos.x - basket.pos.x) < 1.2:
            ball.visible = False
            balls.remove(ball)
            score += 1
        elif ball.pos.y < 0:  # hit the floor
            ball.visible = False
            balls.remove(ball)
            lives -= 1

    score_label.text = f"Score: {score}   Lives: {lives}"
