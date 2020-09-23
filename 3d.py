import math

import pygame

from ray import Ray
from wall import Wall
from walls import bounds

pygame.init()
screen = pygame.display.set_mode((1598, 600), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 15)
gunImg = pygame.image.load('gun.png')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

rays = []
walls = []
origin = (400, 300)
renderA = []
colW = 2
fov = 5
movementS = 4
rotateS = 0.03
mouseSense = 3


def inp():
	global origin
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if chr(event.key) == 'q':
				quit()
	pygame.mouse.set_pos(1200, 300)
	if pygame.mouse.get_pressed()[0]:
		origin = pygame.mouse.get_pos()
	mouseX = pygame.mouse.get_pos()[0]
	if abs(mouseX - 1200) > 2:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, (mouseX - 1200) / 3200 * mouseSense)
	d = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), movementS)
	if pygame.key.get_pressed()[119]:
		origin = tuple(map(sum, zip(origin, d)))
	if pygame.key.get_pressed()[115]:
		origin = tuple(map(sum, zip(origin, rotate((0, 0), d, math.radians(180)))))
	if pygame.key.get_pressed()[97]:
		origin = tuple(map(sum, zip(origin, rotate((0, 0), d, math.radians(-90)))))
	if pygame.key.get_pressed()[100]:
		origin = tuple(map(sum, zip(origin, rotate((0, 0), d, math.radians(90)))))
	if pygame.key.get_pressed()[275]:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, rotateS)
	if pygame.key.get_pressed()[276]:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, -rotateS)


def dist(x1, y1, x2, y2):
	return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def norm(a, div):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / div
	if v == 0:
		return 0
	return a[0] / v, a[1] / v


def getPoints1(r, n):
	return [(math.cos(2 * math.pi / n * x) * r, math.sin(2 * math.pi / n * x) * r) for x in range(0, n + 1)][:int(n // fov)]


def getPoints(y, n):
	a = []
	x = 2 * (y * math.sin(fov / 2) / math.sin(math.pi / 2 - fov / 2)) / (n - 1)
	for i in range(- n // 2, n // 2 + 1):
		a.append((x * i, y))
	return sorted(a, key=lambda x: -x[0])


def rotate(origin, point, angle):
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy


def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)
	return rightMin + (valueScaled * rightSpan)


for b in bounds:
	walls.append(Wall(*b))

for i in getPoints(500, 800 // colW):
	rays.append(Ray(*origin, i))
'''for i in getPoints1(500, 800 // colW * fov):
	rays.append(Ray(*origin, i))'''


def draw():
	global origin
	scene = []
	screen.fill((0, 0, 0))
	# pygame.draw.rect(screen, (55, 146, 71), ((800, 300), (799, 300)))
	# pygame.draw.rect(screen, (168, 237, 242), ((800, 000), (799, 300)))
	pygame.draw.rect(screen, (104, 104, 104), ((800, 300), (799, 300)))
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
		if closest:
			d = dist(*origin, *closest)
			scene.append(d)
			pygame.draw.line(screen, (200, 200, 200), tuple(map(int, r.pos)), closest)

	for b in walls:
		b.show(screen)
	pygame.draw.circle(screen, (0, 255, 0), tuple(map(int, origin)), 5)

	for c in range(len(scene)):
		b = translate(scene[c] ** 2, 0, 800 ** 2, 200, 0)
		h = int(translate(scene[c], 0, 800, 300, 0))
		try:
			pygame.draw.rect(screen, (b, b, b), ((800 + colW * c, 300 - h), (colW, 2 * h)))
		except TypeError:
			pass
	d = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), 50)
	pygame.draw.line(screen, (0, 255, 0), tuple(map(int, origin)), tuple(map(lambda x: int(sum(x)), zip(origin, d))), 3)
	screen.blit(gunImg, (1150, 300))
	fps = str(int(clock.get_fps()))
	screen.blit(font.render(fps, True, (0, 255, 0)), (10, 10))
	pygame.display.update()
	clock.tick(60)


while True:
	inp()
	draw()
