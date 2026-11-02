from vpython import *

scene = canvas(title="Move the Box", width=800, height=500,
               background=color.gray(0.2))
scene.caption = "Click the 3D view first. Arrow keys move the box, A/D spin it."

# A 10 x 10 floor with its top at y = 0, and a box sitting on it
box(pos=vector(0, -0.1, 0), size=vector(10, 0.2, 10), color=color.green)
player = box(pos=vector(0, 0.5, 0), size=vector(1, 1, 1), color=color.cyan)

scene.camera.pos = vector(0, 8, 12)
scene.camera.axis = vector(0, -8, -12)

speed = 0.1
spin = 0.05  # radians per frame

while True:
    rate(60)
    keys = keysdown()  # the keys being held down right now

    # Hold the arrow keys to move the box.
    x = player.pos.x
    z = player.pos.z
    if 'left' in keys:
        x -= speed
    if 'right' in keys:
        x += speed
    if 'up' in keys:
        z -= speed
    if 'down' in keys:
        z += speed

    # Keep the box on the floor.
    x = max(-4.5, min(4.5, x))
    z = max(-4.5, min(4.5, z))
    player.pos = vector(x, 0.5, z)

    # Spin the box around the vertical (y) axis.
    if 'a' in keys:
        player.rotate(angle=spin, axis=vector(0, 1, 0))
    if 'd' in keys:
        player.rotate(angle=-spin, axis=vector(0, 1, 0))
