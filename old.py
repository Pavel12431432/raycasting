import math

import pygame

from ray import Ray
from wall import Wall
from walls import bounds

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 20)
clock = pygame.time.Clock()


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


def dist(x1, y1, x2, y2):
	return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def getPoints(r, n):
	return [(math.cos(2 * math.pi / n * x) * r, math.sin(2 * math.pi / n * x) * r) for x in range(0, n + 1)]


rays = []
verts = [i[:2] for i in bounds]
walls = []
origin = (0, 0)

for b in bounds:
	walls.append(Wall(*b))

for i in getPoints(500, 75):
	rays.append(Ray(*origin, i))


def t(pos):
	return math.atan(pos[1] / pos[0]) if pos[0] != 0 else None


print()


def draw():
	global origin
	screen.fill((0, 0, 0))
	origin = pygame.mouse.get_pos()
	points = []
	for r in rays:
		r.pos = origin
		closest = None
		record = -100
		for b in walls:
			if c := r.cast(b):
				d = c[2]
				if record < d:
					record = d
					closest = c[:2]
		# r.show(screen)
		# pygame.draw.circle(screen, (255, 0, 0), c, 5)
		if closest:
			points.append(closest)
			pygame.draw.line(screen, (200, 200, 200), r.pos, closest)

	# pygame.draw.polygon(screen, (255, 255, 255), points)
	for b in walls:
		b.show(screen)
	pygame.draw.circle(screen, (0, 255, 0), origin, 5)
	fps = str(int(clock.get_fps()))
	screen.blit(font.render(fps, True, (0, 255, 0)), (10, 10))
	pygame.display.update()
	clock.tick(200)


while True:
	inp()
	draw()