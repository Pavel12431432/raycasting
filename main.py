import math

import numpy as np
import pygame

from ray import Ray
from wall import Wall
from walls import bounds

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 15)
clock = pygame.time.Clock()


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


def rotate(point, angle):
	ox, oy = (0, 0)
	px, py = point

	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy


mainRays = []
rightRays = []
leftRays = []

verts = []
for i in bounds:
	verts.append(i[:2])
	verts.append(i[2:])
verts = [list(x) for x in {(tuple(e)) for e in verts}]
walls = [Wall(*b) for b in bounds]
origin = (0, 0)
offset = 0.00001

for i in verts:
	x, y = i[0] - origin[0], i[1] - origin[1]
	mainRays.append(Ray(*origin, (x, y)))

for i in mainRays:
	rightRays.append(Ray(*origin, rotate(i.pos, offset)))
	leftRays.append(Ray(*origin, rotate(i.pos, -offset)))


def t(pos, orig):
	try:
		return np.arctan2(pos[1] - orig[1], pos[0] - orig[0])
	except TypeError:
		return 0


def loop():
	global origin, mainRays, leftRays
	origin = pygame.mouse.get_pos()
	for vertex, lRay, mRay, rRay in zip(verts, leftRays, mainRays, rightRays):
		mRay.direction = (vertex[0] - mRay.pos[0], vertex[1] - mRay.pos[1])
		rRay.direction = rotate(mRay.direction, offset)
		lRay.direction = rotate(mRay.direction, -offset)

	for r in mainRays + rightRays + leftRays:
		r.pos = origin
		r.closest = None
		record = -100
		for b in walls:
			if c := r.cast(b):
				if record < c[2]:
					record = c[2]
					r.closest = c[:2]
	clock.tick(1000)


def draw():
	screen.fill((0, 0, 0))
	for b in walls:
		b.show(screen)
	for r in sorted(rightRays + leftRays, key=lambda r: t(r.closest, r.pos)):
		if r.closest:
			pygame.draw.line(screen, (200, 200, 200), r.pos, r.closest)
			pygame.draw.circle(screen, (0, 255, 0), r.closest, 3)
	text = str(int(clock.get_fps())) + '  ' + str(len(mainRays + leftRays + rightRays))
	screen.blit(font.render(text, True, (255, 0, 0)), (10, 10))
	pygame.draw.circle(screen, (0, 255, 0), origin, 5)
	pygame.display.update()


while True:
	inp()
	loop()
	loop()
	draw()