from vpython import *

scene = canvas(title="3D Shapes", width=900, height=500,
               background=color.gray(0.2))
scene.caption = "Right-drag to rotate the camera, scroll to zoom."

# A long grey floor. Its top is at y = 0, so every shape rests on y = 0.
box(pos=vector(0, -0.1, 0), size=vector(20, 0.2, 4), color=color.gray(0.5))

# Six shapes in a row, 3 units apart, each with its name above it.
box(pos=vector(-7.5, 0.75, 0), size=vector(1.5, 1.5, 1.5), color=color.red)
label(pos=vector(-7.5, 2.5, 0), text="box", box=False)

sphere(pos=vector(-4.5, 0.9, 0), radius=0.9, color=color.green)
label(pos=vector(-4.5, 2.5, 0), text="sphere", box=False)

# Cylinders, cones and pyramids start at pos and grow along axis.
cylinder(pos=vector(-1.5, 0, 0), axis=vector(0, 1.6, 0), radius=0.7, color=color.blue)
label(pos=vector(-1.5, 2.5, 0), text="cylinder", box=False)

cone(pos=vector(1.5, 0, 0), axis=vector(0, 1.8, 0), radius=0.8, color=color.yellow)
label(pos=vector(1.5, 2.5, 0), text="cone", box=False)

pyramid(pos=vector(4.5, 0, 0), axis=vector(0, 1.6, 0), size=vector(1.6, 1.6, 1.6),
        color=color.orange)
label(pos=vector(4.5, 2.5, 0), text="pyramid", box=False)

# A ring's axis points through its hole; this one faces the camera.
ring(pos=vector(7.5, 0.9, 0), axis=vector(0, 0, 1), radius=0.7, thickness=0.2,
     color=color.magenta)
label(pos=vector(7.5, 2.5, 0), text="ring", box=False)

# Camera in front and a little above, aimed at the middle of the row
scene.camera.pos = vector(0, 4, 13)
scene.camera.axis = vector(0, -3, -13)

print("Scene is open in your browser. Close the tab or press Ctrl+C to stop.")

# Keep the program running so the browser tab stays open.
while True:
    rate(30)
