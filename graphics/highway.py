
from vpython import *

# Create window
scene = canvas(
    title="3D Highway Camera Simulator",
    width=1000,
    height=600,
    background=vector(0.5, 0.7, 1)
)

scene.autoscale = False
scene.range = 16

# Create grass
grass = box(
    pos=vector(0, -1.2, -15),
    size=vector(35, 0.1, 45),
    color=color.green
)

# Create road
road = box(
    pos=vector(0, -1, -15),
    size=vector(7, 0.2, 40),
    color=color.gray(0.3)
)

# Create road markings
for z in range(2, -32, -4):
    box(
        pos=vector(0, -0.85, z),
        size=vector(0.2, 0.03, 2),
        color=color.yellow
    )

# Create trees
for z in range(0, -31, -6):
    for x in [-7, 7]:
        cylinder(
            pos=vector(x, -1, z),
            axis=vector(0, 2, 0),
            radius=0.3,
            color=color.orange
        )

        sphere(
            pos=vector(x, 2, z),
            radius=1.5,
            color=color.green
        )

# Camera function
def set_camera(position, target, top=False):
    if top:
        scene.up = vector(0, 0, -1)
    else:
        scene.up = vector(0, 1, 0)

    scene.camera.pos = position
    scene.camera.axis = target - position

# Default camera
set_camera(
    vector(0, 2, 12),
    vector(0, 0, -15)
)

# Camera buttons
scene.append_to_caption("\n\nCAMERA VIEWS\n")

def driver_view(b):
    set_camera(
        vector(0, 2, 12),
        vector(0, 0, -15)
    )

def top_view(b):
    set_camera(
        vector(0, 30, -15),
        vector(0, 0, -15),
        True
    )

def side_view(b):
    set_camera(
        vector(20, 8, -15),
        vector(0, 0, -15)
    )

def diagonal_view(b):
    set_camera(
        vector(15, 10, 10),
        vector(0, 0, -15)
    )

button(text="Driver", bind=driver_view)
button(text="Top", bind=top_view)
button(text="Side", bind=side_view)
button(text="Diagonal", bind=diagonal_view)

# Movement controls
scene.append_to_caption("\n\nCAMERA MOVEMENT\n")

def forward(b):
    scene.camera.pos += vector(0, 0, -2)

def backward(b):
    scene.camera.pos += vector(0, 0, 2)

button(text="Forward", bind=forward)
button(text="Backward", bind=backward)

# Numerical projection
print("\nPROJECTION COMPARISON")

f = 2

for z in [5, 10, 20]:
    x = 2
    y = 1

    perspective_x = f * x / z
    perspective_y = f * y / z

    print("\nDepth:", z)
    print("Orthographic:", x, y)
    print("Perspective:",
          round(perspective_x, 2),
          round(perspective_y, 2))

# Keep program running
while True:
    rate(60)
