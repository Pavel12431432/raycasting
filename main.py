import math

import pygame

from ray import Ray
from wall import Wall
from walls import bounds
import numpy as np

pygame.init()
screen = pygame.display.set_mode((825, 625), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 15)
clock = pygame.time.Clock()


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


def rotate(origin, point, angle):
	ox, oy = origin
	px, py = point

	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy


mainRays = []
rightRays = []
leftRays = []

verts = [i[:2] for i in bounds]
walls = []
origin = (0, 0)
offset = 0.00001

for b in bounds:
	walls.append(Wall(*b))

for i in verts:
	x, y = i[0] - origin[0], i[1] - origin[1]
	ang = 0.5
	mainRays.append(Ray(*origin, (x, y)))

for i in mainRays:
	rightRays.append(Ray(*origin, rotate((0, 0), i.pos, offset)))
	leftRays.append(Ray(*origin, rotate((0, 0), i.pos, -offset)))


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
		rRay.direction = rotate((0, 0), mRay.direction, offset)
		lRay.direction = rotate((0, 0), mRay.direction, -offset)

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
