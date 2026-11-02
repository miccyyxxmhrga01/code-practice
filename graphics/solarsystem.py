from vpython import *

# Create scene
scene = canvas(
    title="3D Solar System Camera Simulator",
    width=1000,
    height=600,
    background=color.black
)

scene.autoscale = False
scene.range = 12

# Create Sun
sun = sphere(
    pos=vector(0, 0, 0),
    radius=2,
    color=color.orange,
    emissive=True
)

# Create Earth
earth = sphere(
    pos=vector(5, 0, 0),
    radius=1,
    color=color.blue
)

# Create Mars
mars = sphere(
    pos=vector(9, 0, 0),
    radius=0.7,
    color=color.red
)

# Add labels
label(pos=vector(0, 3, 0), text="SUN", box=False)
label(pos=vector(5, 2, 0), text="EARTH", box=False)
label(pos=vector(9, 2, 0), text="MARS", box=False)

# Camera function
def change_camera(position, target):
    scene.camera.pos = position
    scene.camera.axis = target - position

# Camera target
target = vector(4, 0, 0)

# Default camera
change_camera(vector(4, 5, 20), target)

# Camera controls
scene.append_to_caption("\n\nCAMERA CONTROLS\n")

def front_view(b):
    change_camera(vector(4, 5, 20), target)

def top_view(b):
    change_camera(vector(4, 20, 0), target)

def side_view(b):
    change_camera(vector(20, 5, 0), target)

def diagonal_view(b):
    change_camera(vector(15, 10, 15), target)

button(text="Front", bind=front_view)
button(text="Top", bind=top_view)
button(text="Side", bind=side_view)
button(text="Diagonal", bind=diagonal_view)

# Camera movement
scene.append_to_caption("\n\nMOVE CAMERA\n")

def move_left(b):
    scene.camera.pos += vector(-2, 0, 0)

def move_right(b):
    scene.camera.pos += vector(2, 0, 0)

def move_up(b):
    scene.camera.pos += vector(0, 2, 0)

def move_down(b):
    scene.camera.pos += vector(0, -2, 0)

button(text="Left", bind=move_left)
button(text="Right", bind=move_right)
button(text="Up", bind=move_up)
button(text="Down", bind=move_down)

# Numerical projection example
f = 2

print("PERSPECTIVE PROJECTION")

for z in [4, 8, 12]:
    x = 2
    y = 1

    projected_x = f * x / z
    projected_y = f * y / z

    print("Depth:", z)
    print("2D:", projected_x, projected_y)

# Keep the program running
while True:
    rate(60)