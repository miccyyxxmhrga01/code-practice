from vpython import *

scene = canvas(title="3D Scene and Camera", width=800, height=500,
               background=color.gray(0.2))
scene.caption = "Right-drag to rotate the camera, scroll to zoom."

# Three boxes of increasing size, all resting on the same floor (y = 0).
box(pos=vector(-2, 0.5, 0), size=vector(1, 1, 1), color=color.red)
box(pos=vector(0, 1, 0), size=vector(2, 2, 2), color=color.green)
box(pos=vector(3, 1.5, 0), size=vector(3, 3, 3), color=color.blue)

# Place the camera, then aim it at the middle of the group of boxes.
scene.camera.pos = vector(8, 5, 10)
scene.camera.axis = vector(-5,-2,-5)

print("Scene is open in your browser. Close the tab or press Ctrl+C to stop.")

# Keep the program running so the browser tab stays open.
while True:
    rate(30)
