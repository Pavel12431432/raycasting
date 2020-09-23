import math
from datetime import datetime

import pygame

from ray import Ray
from wall import Wall
from walls import bounds

pygame.init()
screen = pygame.display.set_mode((1601, 601), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 15)
pygame.mouse.set_visible(False)
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

skyImg = pygame.image.load('sky.png')

rays = []
scene = []
walls = [Wall(*b) for b in bounds]
origin = (400, 300)
colW = 4
fov = 5  # math.radians(72)
movementS = 1.75
rotateS = 0.03
mouseSense = 3
delta = datetime.now()
blockHeight = 8
paused = False

distanceToPPlane = 400 / math.tan(math.radians(180 / fov))


def inp():
	global origin, delta, paused
	if not (timedelta := abs(delta - datetime.now()).microseconds / 16666.66):
		timedelta = 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if chr(event.key) == 'q':
				quit()
			elif event.key == 27:
				paused = not paused
				pygame.mouse.set_visible(paused)

	if not paused and pygame.key.get_focused():
		pygame.mouse.set_pos(1200, 300)
	if pygame.mouse.get_pressed()[0]:
		origin = pygame.mouse.get_pos()
	mouseX = pygame.mouse.get_pos()[0]
	if abs(mouseX - 1200) > 0 and not paused:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, (mouseX - 1200) / 3200 * mouseSense)
	d = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), movementS * timedelta)
	nextPos = origin
	if pygame.key.get_pressed()[119]:
		nextPos = tuple(map(sum, zip(nextPos, d)))
	if pygame.key.get_pressed()[115]:
		nextPos = tuple(map(sum, zip(nextPos, rotate((0, 0), d, math.radians(180)))))
	if pygame.key.get_pressed()[97]:
		nextPos = tuple(map(sum, zip(nextPos, rotate((0, 0), d, math.radians(-90)))))
	if pygame.key.get_pressed()[100]:
		nextPos = tuple(map(sum, zip(nextPos, rotate((0, 0), d, math.radians(90)))))
	nextPos = (constrain(nextPos[0], 1, 798), constrain(nextPos[1], 1, 598))
	origin = nextPos

	if pygame.key.get_pressed()[275]:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, rotateS * timedelta)
	if pygame.key.get_pressed()[276]:
		for r in rays:
			r.direction = rotate((0, 0), r.direction, -rotateS * timedelta)
	delta = datetime.now()


def dist(x1, y1, x2, y2):
	return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def ang(a, b):
	dotp = sum(map(lambda x: x[0] * x[1], zip(a, b)))
	m1 = math.sqrt(a[0] ** 2 + a[1] ** 2)
	m2 = math.sqrt(b[0] ** 2 + b[1] ** 2)
	if not m1 * m2: return 0
	return dotp / (m1 * m2)


def constrain(value, min, max):
	if value < min: value = min
	if value > max: value = max
	return value


def norm(a, div):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / div
	if v == 0:
		return 0
	return a[0] / v, a[1] / v


def getPoints1(r, n):
	return [(math.cos(2 * math.pi / n * x) * r, math.sin(2 * math.pi / n * x) * r) for x in range(0, n + 1)][
		   :int(n // fov)]


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


for i in getPoints1(500, 800 // colW * fov):
	rays.append(Ray(*origin, i))


def loop():
	global origin, scene
	scene = []
	looking = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), 1)
	for r in rays:
		r.pos = origin
		r.closest = None
		record = -100
		wall = None
		for b in walls:
			if c := r.cast(b):
				u = c[2]
				if record < u:
					record = u
					r.closest = c[:2]
					wall = b
		if r.closest:
			cl = tuple(map(lambda x: x[0] - x[1], zip(r.closest, origin)))
			a = ang(looking, cl)
			d = dist(*origin, *r.closest)
			if r.closest[0] % 25 == 0:
				spriteIndex = r.closest[1] % 25
			else:
				spriteIndex = r.closest[0] % 25
			sprite = wall.sprite
			scene.append((d * a, wall.color, spriteIndex, sprite))


def draw():
	global scene
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (50, 70, 70), ((800, 300), (799, 300)))
	screen.blit(skyImg, (800, 0))
	for r in rays:
		if r.closest:
			pygame.draw.line(screen, (200, 200, 200), tuple(map(int, r.pos)), r.closest)
	for b in walls:
		b.show(screen)

	for c in range(len(scene)):
		h = int(constrain(blockHeight / scene[c][0] * distanceToPPlane, 0, 300))
		# b = translate(constrain(h * 5, 0, 300), 0, 300, 0.1, 0.9)
		b = translate(scene[c][2], 0, 24, 0, 4)
		try:
			'''pygame.draw.rect(screen, tuple(map(lambda x: x[0] * x[1], zip((b, b, b), scene[c][1]))),
							((800 + colW * c, 300 - h), (colW, 2 * h)))'''
			# pygame.draw.rect(screen, (b, b, b), ((800 + colW * c + 1, 300 - h), (colW, 2 * h)))
			# screen.blit(wallImg, (0, 0), (0, 0, 5, 25))
			img = pygame.transform.scale(scene[c][3], (100, 2 * h))
			# screen.blit(img, (0, 0))
			screen.blit(img, (800 + colW * c + 1, 300 - h), (24 * b, 0, 4, 2 * h))
		# screen.blit(font.render(str(b)))
		except TypeError:
			pass
	looking = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), 50)
	pygame.draw.line(screen, (0, 255, 0), tuple(map(int, origin)),
					 tuple(map(lambda x: int(sum(x)), zip(origin, looking))), 3)
	screen.blit(font.render(str(int(clock.get_fps())), True, (0, 255, 0)), (10, 10))
	pygame.display.update()


while True:
	inp()
	loop()
	draw()
	clock.tick(144)