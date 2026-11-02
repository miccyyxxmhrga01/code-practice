
from vpython import *

# Create scene
scene = canvas(
    title="3D Mini City - Drone Camera Explorer",
    width=1000,
    height=600,
    background=vector(0.55, 0.75, 1)
)

scene.autoscale = False
scene.range = 20
scene.center = vector(0, 0, -8)

# Ground
box(
    pos=vector(0, -1.2, -8),
    size=vector(40, 0.3, 42),
    color=color.green
)

# Road
box(
    pos=vector(0, -1, -8),
    size=vector(8, 0.1, 38),
    color=color.gray(0.25)
)

# Road markings
for z in range(8, -25, -5):
    box(
        pos=vector(0, -0.92, z),
        size=vector(0.2, 0.03, 2),
        color=color.yellow
    )

# Buildings
building_colors = [
    color.cyan,
    color.orange,
    color.magenta
]

for i, z in enumerate([1, -8, -17]):
    for x in [-11, 11]:
        height = 5 + i * 2

        box(
            pos=vector(x, height / 2 - 1, z),
            size=vector(5, height, 5),
            color=building_colors[i]
        )

        # Building roof
        box(
            pos=vector(x, height - 0.9, z),
            size=vector(5.5, 0.3, 5.5),
            color=color.gray(0.3)
        )

# Three identical cars
car_positions = [
    vector(-2, -0.35, 3),
    vector(2, -0.35, -6),
    vector(-2, -0.35, -15)
]

car_colors = [color.red, color.blue, color.yellow]

for i in range(3):
    p = car_positions[i]

    box(
        pos=p,
        size=vector(1.8, 0.7, 3),
        color=car_colors[i]
    )

    box(
        pos=p + vector(0, 0.55, 0),
        size=vector(1.4, 0.5, 1.5),
        color=color.white
    )

# Trees
for z in range(5, -22, -7):
    for x in [-6, 6]:
        cylinder(
            pos=vector(x, -1, z),
            axis=vector(0, 2, 0),
            radius=0.25,
            color=vector(0.45, 0.25, 0.1)
        )

        sphere(
            pos=vector(x, 1.7, z),
            radius=1.2,
            color=color.green
        )

# Camera target
target = vector(0, 0, -8)

# Camera function
def set_camera(position, look_at, top=False):
    if top:
        scene.up = vector(0, 0, -1)
    else:
        scene.up = vector(0, 1, 0)

    scene.camera.pos = position
    scene.camera.axis = look_at - position

# Initial view
set_camera(vector(15, 12, 20), target)

# Camera buttons
scene.append_to_caption("\n\nCAMERA VIEWS\n")

def front_view(b):
    set_camera(vector(0, 5, 22), target)

def side_view(b):
    set_camera(vector(25, 9, -8), target)

def top_view(b):
    set_camera(vector(0, 30, -8), target, True)

def diagonal_view(b):
    set_camera(vector(15, 12, 20), target)

button(text="Front", bind=front_view)
button(text="Side", bind=side_view)
button(text="Top", bind=top_view)
button(text="Diagonal", bind=diagonal_view)

# Camera movement
scene.append_to_caption("\n\nDRONE MOVEMENT\n")

def move_forward(b):
    scene.camera.pos += norm(scene.camera.axis) * 2

def move_backward(b):
    scene.camera.pos -= norm(scene.camera.axis) * 2

def move_up(b):
    scene.camera.pos += vector(0, 2, 0)

def move_down(b):
    scene.camera.pos += vector(0, -2, 0)

button(text="Forward", bind=move_forward)
button(text="Backward", bind=move_backward)
button(text="Up", bind=move_up)
button(text="Down", bind=move_down)

# Numerical projection
print("\nPROJECTION COMPARISON")

f = 2

for z in [5, 10, 20]:
    x = 2
    y = 1

    px = f * x / z
    py = f * y / z

    print("\nDepth:", z)
    print("Orthographic:", x, y)
    print("Perspective:", round(px, 2), round(py, 2))

# Keep program running
while True:
    rate(60)
