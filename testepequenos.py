import pgzero
import pgzrun

WIDTH = 800
HEIGHT = 800

img = Actor("enemy_robot_walk0", (300, 300))


img.image = "enemy_robot_walk0"
img.flip_x(img)
def draw():
    img.draw()
pgzrun.go()