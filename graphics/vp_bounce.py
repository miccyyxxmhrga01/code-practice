from vpython import *

scene = canvas(title="Bouncing Ball", width=800, height=500,
               background=color.gray(0.2))
scene.caption = "A dropped ball loses a little height on every bounce, then gets dropped again."

# Floor with its top at y = 0
box(pos=vector(0, -0.1, 0), size=vector(10, 0.2, 4), color=color.green)

START_HEIGHT = 6
ball = sphere(pos=vector(-4, START_HEIGHT, 0), radius=0.5, color=color.red,
              make_trail=True, trail_type="points", interval=5, retain=60)

velocity = vector(1, 0, 0)  # drifts right so the bounces spread out
gravity = vector(0, -9.8, 0)
dt = 0.01

scene.camera.pos = vector(0, 4, 14)
scene.camera.axis = vector(0, -1, -14)

while True:
    rate(100)  # 100 steps per second, matching dt = 0.01

    # Gravity changes the velocity, and the velocity changes the position.
    velocity += gravity * dt
    ball.pos += velocity * dt

    # Bounce when the ball touches the floor, keeping 80% of its speed
    if ball.pos.y - ball.radius < 0:
        ball.pos = vector(ball.pos.x, ball.radius, 0)
        velocity.y = -velocity.y * 0.8

        # Almost stopped bouncing, so drop it again from the top
        if velocity.y < 0.5:
            ball.pos = vector(ball.pos.x, START_HEIGHT, 0)
            velocity.y = 0
            ball.clear_trail()

    # Turn around at the ends of the floor
    if abs(ball.pos.x) > 5 - ball.radius:
        velocity.x = -velocity.x
