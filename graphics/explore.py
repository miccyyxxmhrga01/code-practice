from vpython import *

scene = canvas(
    title="3D Camera Test",
    width=900,
    height=600,
    background=color.black
)

box(
    pos=vector(-3, 0, 0),
    color=color.red
)

box(
    pos=vector(0, 0, 0),
    color=color.green
)

box(
    pos=vector(3, 0, 0),
    color=color.blue
)

scene.camera.pos = vector(0, 3, 12)
scene.camera.axis = vector(0, -3, -12)

while True:
    rate(60)