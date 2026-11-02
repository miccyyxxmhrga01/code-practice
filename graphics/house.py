
from vpython import *

# Create 3D scene
scene = canvas(
    title="3D Mountain House - Camera Explorer",
    width=1000,
    height=650,
    background=vector(0.55, 0.75, 1)
)

scene.autoscale = False
scene.range = 25
scene.center = vector(0, 2, -15)

# Ground
ground = box(
    pos=vector(0, -2.2, -25),
    size=vector(100, 0.35, 100),
    color=vector(0.30, 0.65, 0.25)
)

# Mountains
mountains = [
    (-30, 20, 15),
    (-15, 25, 17),
    (5, 22, 15),
    (23, 28, 18),
    (40, 20, 14)
]

for x, height, radius in mountains:
    cone(
        pos=vector(x, -2, -48),
        axis=vector(0, height, 0),
        radius=radius,
        color=vector(0.40, 0.49, 0.47)
    )

    # Snow cap
    cone(
        pos=vector(x, -2 + height * 0.72, -48),
        axis=vector(0, height * 0.28, 0),
        radius=radius * 0.28,
        color=color.white
    )

# House walls
house = box(
    pos=vector(0, 0, -7),
    size=vector(9, 4, 7),
    color=vector(0.95, 0.82, 0.62)
)

# Roof
roof = pyramid(
    pos=vector(0, 2, -7),
    axis=vector(0, 2.5, 0),
    size=vector(2.5, 8, 10),
    up=vector(0, 0, 1),
    color=vector(0.65, 0.16, 0.12)
)

# Door
door = box(
    pos=vector(0, -0.8, -3.43),
    size=vector(1.8, 2.4, 0.12),
    color=vector(0.42, 0.22, 0.10)
)

# Door knob
sphere(
    pos=vector(0.6, -0.8, -3.33),
    radius=0.10,
    color=color.yellow
)

# Windows
for x in [-2.8, 2.8]:
    box(
        pos=vector(x, 0.3, -3.40),
        size=vector(2, 1.8, 0.13),
        color=color.white
    )

    box(
        pos=vector(x, 0.3, -3.30),
        size=vector(1.65, 1.45, 0.08),
        color=vector(0.25, 0.65, 0.95)
    )

    box(
        pos=vector(x, 0.3, -3.23),
        size=vector(0.12, 1.45, 0.08),
        color=color.white
    )

# Path to house
box(
    pos=vector(0, -1.99, 3),
    size=vector(2.5, 0.06, 13),
    color=vector(0.72, 0.66, 0.55)
)

# Trees
tree_positions = [
    (-13, -3), (-17, -13),
    (13, -4), (17, -15),
    (-10, -23), (12, -24)
]

for x, z in tree_positions:
    cylinder(
        pos=vector(x, -2, z),
        axis=vector(0, 2.5, 0),
        radius=0.35,
        color=vector(0.45, 0.25, 0.12)
    )

    cone(
        pos=vector(x, -0.5, z),
        axis=vector(0, 4.5, 0),
        radius=2,
        color=vector(0.08, 0.42, 0.18)
    )

# Sun
sphere(
    pos=vector(-35, 35, -55),
    radius=4,
    color=color.yellow,
    emissive=True
)

# Camera function
def set_camera(position, target, top=False):
    if top:
        scene.up = vector(0, 0, -1)
    else:
        scene.up = vector(0, 1, 0)

    scene.camera.pos = position
    scene.camera.axis = target - position

# Initial camera view
target = vector(0, 1, -15)

set_camera(
    vector(16, 9, 24),
    target
)

# Camera views
scene.append_to_caption("\n\nCAMERA VIEWS\n")

def front_view(b):
    set_camera(
        vector(0, 6, 25),
        vector(0, 1, -15)
    )

def side_view(b):
    set_camera(
        vector(28, 7, -7),
        vector(0, 0, -7)
    )

def top_view(b):
    set_camera(
        vector(0, 35, 8),
        vector(0, 0, -12),
        True
    )

def diagonal_view(b):
    set_camera(
        vector(16, 9, 24),
        target
    )

button(text="Front", bind=front_view)
button(text="Side", bind=side_view)
button(text="Top", bind=top_view)
button(text="Diagonal", bind=diagonal_view)

# Camera movement
scene.append_to_caption("\n\nCAMERA MOVEMENT\n")

def move_forward(b):
    scene.camera.pos += norm(scene.camera.axis) * 2

def move_backward(b):
    scene.camera.pos -= norm(scene.camera.axis) * 2

def move_left(b):
    scene.camera.pos += vector(-2, 0, 0)

def move_right(b):
    scene.camera.pos += vector(2, 0, 0)

button(text="Forward", bind=move_forward)
button(text="Backward", bind=move_backward)
button(text="Left", bind=move_left)
button(text="Right", bind=move_right)

# Numerical projection
print("\n3D PROJECTION COMPARISON")

f = 2.0

for z in [5, 10, 20]:
    x = 2
    y = 1

    px = f * x / z
    py = f * y / z

    print("\nDepth:", z)
    print("Orthographic:", x, y)
    print("Perspective:", round(px, 2), round(py, 2))

# Keep scene running
while True:
    rate(60)
