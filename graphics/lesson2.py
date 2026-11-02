from vpython import *

scene = canvas(title="Virtual Camera")

sphere(pos=vector(0,0,0), radius=1 ,color=color.yellow)

scene.camera.pos = vector(0,0,10)
scene.camera.axis = vector(0,0,-10)

while True:
    rate(30)