from vpython import *
from math import pi, cos, sin, radians
import random

# Solar System v2
# All 8 planets (plus the dwarf planet Pluto) orbit the Sun at their real relative speeds.
# Sizes and distances are NOT to scale (the real ones would not fit on screen),
# but the orbit periods are real, so Mercury laps the Sun ~4 times per Earth year
# and Neptune takes almost 165 years.

# Create scene
scene = canvas(
    title="3D Solar System v2",
    width=1000,
    height=600,
    background=color.black
)

scene.autoscale = False
scene.range = 30
scene.center = vector(0, 0, 0)
scene.forward = vector(0, -0.5, -1)

# Light comes from the Sun instead of VPython's default lights,
# so each planet has a bright day side and a dark night side.
scene.lights = []
local_light(pos=vector(0, 0, 0), color=color.white)
scene.ambient = color.gray(0.25)

# Background stars, scattered on a big sphere around everything.
# Kept within 60 units because VPython hides objects beyond 10x the camera distance.
stars = []
for i in range(400):
    direction = vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
    stars.append(60 * norm(direction))
points(pos=stars, radius=1.5, color=color.white)

# Create Sun (emissive means it glows and is not darkened by the light)
sun = sphere(
    pos=vector(0, 0, 0),
    radius=2,
    color=color.orange,
    emissive=True
)
sun_glow = sphere(
    pos=vector(0, 0, 0),
    radius=2.6,
    color=color.yellow,
    opacity=0.15,
    emissive=True
)

# Planet data
#   orbit  = distance from the Sun in scene units
#   size   = sphere radius in scene units
#   period = time for one orbit, in Earth years (real values)
#   au, km = real distance from the Sun and real diameter, shown when clicked
#   tilt   = how many degrees the orbit is tilted (0 if left out)
planet_data = [
    {"name": "Mercury", "orbit": 4.0,  "size": 0.30, "period": 0.24,
     "color": color.gray(0.6),           "au": 0.39, "km": 4879},
    {"name": "Venus",   "orbit": 5.5,  "size": 0.50, "period": 0.62,
     "color": vector(0.95, 0.8, 0.5),    "au": 0.72, "km": 12104},
    {"name": "Earth",   "orbit": 7.0,  "size": 0.55, "period": 1.00,
     "color": color.white,               "au": 1.00, "km": 12742},
    {"name": "Mars",    "orbit": 8.7,  "size": 0.40, "period": 1.88,
     "color": vector(0.85, 0.35, 0.2),   "au": 1.52, "km": 6779},
    {"name": "Jupiter", "orbit": 13.5, "size": 1.20, "period": 11.86,
     "color": vector(0.85, 0.7, 0.5),    "au": 5.20, "km": 139820},
    {"name": "Saturn",  "orbit": 17.0, "size": 1.00, "period": 29.46,
     "color": vector(0.9, 0.8, 0.55),    "au": 9.58, "km": 116460},
    {"name": "Uranus",  "orbit": 20.5, "size": 0.75, "period": 84.01,
     "color": vector(0.6, 0.9, 0.95),    "au": 19.2, "km": 50724},
    {"name": "Neptune", "orbit": 23.5, "size": 0.72, "period": 164.8,
     "color": vector(0.3, 0.45, 0.95),   "au": 30.1, "km": 49244},
    # Pluto is a dwarf planet. Its orbit is tilted 17 degrees from the planets' orbits.
    {"name": "Pluto",   "orbit": 27.0, "size": 0.25, "period": 248.0,
     "color": vector(0.8, 0.7, 0.6),     "au": 39.5, "km": 2377, "tilt": 17},
]

# Create the planets, their orbit lines and their labels
planets = []
orbit_lines = []
labels = []

for data in planet_data:
    planet = sphere(
        pos=vector(data["orbit"], 0, 0),
        radius=data["size"],
        color=data["color"]
    )
    if data["name"] == "Earth":
        planet.texture = textures.earth

    # Each planet starts at a random point on its orbit
    data["start_angle"] = random.uniform(0, 2 * pi)

    # A ring's axis points straight out of its flat side, so tilting
    # the axis around the x-axis tilts the whole orbit line.
    tilt = radians(data.get("tilt", 0))
    orbit_lines.append(ring(
        pos=vector(0, 0, 0),
        axis=vector(0, cos(tilt), sin(tilt)),
        radius=data["orbit"],
        thickness=0.02,
        color=color.gray(0.35)
    ))
    labels.append(label(
        pos=planet.pos,
        text=data["name"],
        yoffset=18,
        height=12,
        box=False,
        line=False,
        color=color.white
    ))
    planets.append(planet)

earth = planets[2]
saturn = planets[5]

# Saturn's rings: three thin rings, tilted a little
saturn_rings = []
for r, shade in [(1.45, 0.75), (1.7, 0.85), (1.95, 0.65)]:
    saturn_rings.append(ring(
        pos=saturn.pos,
        axis=vector(0.35, 1, 0),
        radius=r,
        thickness=0.06,
        color=vector(0.9, 0.8, 0.6) * shade
    ))

# The Moon orbits the Earth once every 27.3 days
moon_period = 27.3 / 365.25
moon_distance = 1.1
moon = sphere(
    pos=earth.pos + vector(moon_distance, 0, 0),
    radius=0.15,
    color=color.gray(0.75)
)

# Asteroid belt between Mars and Jupiter
asteroids = []
for i in range(300):
    angle = random.uniform(0, 2 * pi)
    distance = random.uniform(10.2, 11.6)
    height = random.uniform(-0.25, 0.25)
    asteroids.append(vector(distance * cos(angle), height, distance * sin(angle)))
points(pos=asteroids, radius=2, color=color.gray(0.55))

# Info shown when an object is clicked
info = {}
for planet, data in zip(planets, planet_data):
    info[planet] = (data["name"] + ": " + str(data["au"]) + " AU from the Sun, "
                    + format(data["km"], ",") + " km wide, one orbit = "
                    + str(data["period"]) + " Earth years")
info[planets[8]] = ("Pluto: a dwarf planet (not a full planet since 2006), "
                    + info[planets[8]][len("Pluto: "):])
info[sun] = "Sun: a star 1,392,700 km wide. It holds 99.8% of the Solar System's mass."
info[sun_glow] = info[sun]
info[moon] = "Moon: 3,474 km wide, orbits the Earth every 27.3 days"
for r in saturn_rings:
    info[r] = "Saturn's rings: billions of pieces of ice and rock"

# Simulation state
years_per_second = 0.1
paused = False
sim_years = 0.0

# ---------------- Controls ----------------
scene.caption = ("Right-drag (or Ctrl+drag) to rotate, scroll to zoom, "
                 "click a planet for facts.\n\n")

# Pause / play
def toggle_pause(b):
    global paused
    paused = not paused
    if paused:
        b.text = "Play"
    else:
        b.text = "Pause"

button(text="Pause", bind=toggle_pause)
scene.append_to_caption("   ")

# Speed slider
def set_speed(s):
    global years_per_second
    years_per_second = s.value
    speed_text.text = "{:.2f} Earth years per second".format(s.value)

scene.append_to_caption("Speed: ")
slider(min=0.02, max=10, value=years_per_second, length=300, bind=set_speed)
speed_text = wtext(text="{:.2f} Earth years per second".format(years_per_second))

scene.append_to_caption("\n\nTime passed: ")
time_text = wtext(text="0.00 years")

# Camera views
scene.append_to_caption("\n\nCAMERA VIEWS   ")

def stop_following():
    scene.camera.follow(None)
    scene.center = vector(0, 0, 0)
    follow_menu.selected = "Nothing"

def top_view(b):
    stop_following()
    scene.forward = vector(0, -1, -0.01)  # tiny z so "up" is never parallel to forward
    scene.range = 30

def side_view(b):
    stop_following()
    scene.forward = vector(0, -0.05, -1)
    scene.range = 30

def angled_view(b):
    stop_following()
    scene.forward = vector(0, -0.5, -1)
    scene.range = 30

button(text="Top", bind=top_view)
button(text="Side", bind=side_view)
button(text="Angled", bind=angled_view)

# Follow a planet with the camera
scene.append_to_caption("   Follow: ")

def choose_follow(m):
    if m.selected == "Nothing":
        scene.camera.follow(None)
        scene.center = vector(0, 0, 0)
        scene.range = 30
        return
    if m.selected == "Sun":
        target = sun
    else:
        names = [data["name"] for data in planet_data]
        target = planets[names.index(m.selected)]
    scene.camera.follow(target)
    # Zoom in, but not so far that the stars get clipped
    scene.range = max(8, target.radius * 6)

follow_menu = menu(
    choices=["Nothing", "Sun"] + [data["name"] for data in planet_data],
    selected="Nothing",
    bind=choose_follow
)

# Show / hide orbit lines and labels
scene.append_to_caption("\n\n")

def toggle_orbits(c):
    for line in orbit_lines:
        line.visible = c.checked

def toggle_labels(c):
    for lab in labels:
        lab.visible = c.checked

checkbox(text="Show orbits ", checked=True, bind=toggle_orbits)
checkbox(text="Show labels", checked=True, bind=toggle_labels)

scene.append_to_caption("\n\n")
info_text = wtext(text="Click any planet, the Sun or the Moon.")

# Click to show info
def on_click():
    obj = scene.mouse.pick
    if obj in info:
        info_text.text = info[obj]

scene.bind("click", on_click)

# ---------------- Animation ----------------
dt = 1 / 60

while True:
    rate(60)
    if paused:
        continue

    sim_years += years_per_second * dt

    # Each planet's angle comes straight from the time:
    # one full turn (2*pi) every "period" years.
    for planet, data, lab in zip(planets, planet_data, labels):
        angle = data["start_angle"] + 2 * pi * sim_years / data["period"]
        r = data["orbit"]
        tilt = radians(data.get("tilt", 0))
        # Flat circle (x, z), then tilted around the x-axis (only Pluto has a tilt)
        planet.pos = vector(r * cos(angle),
                            r * sin(angle) * sin(tilt),
                            -r * sin(angle) * cos(tilt))
        lab.pos = planet.pos

        # The real Earth spins 365 times a year, far too fast to see,
        # so every planet just spins slowly for show.
        planet.rotate(angle=2 * pi * years_per_second * dt, axis=vector(0, 1, 0))

    for r in saturn_rings:
        r.pos = saturn.pos

    moon_angle = 2 * pi * sim_years / moon_period
    moon.pos = earth.pos + moon_distance * vector(cos(moon_angle), 0, -sin(moon_angle))

    time_text.text = "{:.2f} years".format(sim_years)


