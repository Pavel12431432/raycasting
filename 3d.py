import math
from datetime import datetime

import pygame

from ray import Ray
from wall import Wall
from walls import bounds

pygame.init()
screen = pygame.display.set_mode((1600, 601), 0, 32)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 15)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

scene = []
walls = [Wall(*b) for b in bounds]
origin = (400, 300)
colW = 2
fov = 5
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
	nextPos = (min(max(nextPos[0], 1), 798), min(max(nextPos[1], 1), 598))
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
	return 0 if not m1 * m2 else dotp / (m1 * m2)


def norm(a, div):
	v = math.sqrt(a[0] ** 2 + a[1] ** 2) / div
	if v == 0:
		return 0
	return a[0] / v, a[1] / v


def get_points(r, n):
	return [(math.cos(2 * math.pi / n * x) * r, math.sin(2 * math.pi / n * x) * r) for x in range(0, n + 1)][
		   :int(n // fov)]


def rotate(o, point, angle):
	ox, oy = o
	px, py = point
	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy


def translate(value, left_min, left_max, right_min, right_max):
	leftSpan = left_max - left_min
	rightSpan = right_max - right_min
	valueScaled = float(value - left_min) / float(leftSpan)
	return right_min + (valueScaled * rightSpan)


rays = [Ray(*origin, i) for i in get_points(500, 800 // colW * fov)]
angle_between_rays = math.cos(math.radians(360 / fov / len(rays)))


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
			spriteIndex = r.closest[1] % 25 if not r.closest[0] % 25 else r.closest[0] % 25
			sprite = wall.sprite
			scene.append((d * a, wall.color, spriteIndex, sprite))


def draw():
	global scene
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (170, 170, 170), ((800, 0), (799, 300)))
	pygame.draw.rect(screen, (50, 70, 70), ((800, 300), (799, 300)))

	looking = norm(tuple(map(sum, zip(rays[0].direction, rays[-1].direction))), 50)

	for r in rays:
		if r.closest:
			pygame.draw.line(screen, (200, 200, 200), tuple(map(int, r.pos)), r.closest)
	for b in walls:
		b.show(screen)

	for c in range(len(scene)):
		h = round(min(max(blockHeight / scene[c][0] * distanceToPPlane, 0), 300))
		b = scene[c][2] * colW
		size = 1
		if not c == len(scene) - 1:
			alpha = min(ang(looking, rays[c].direction), ang(looking, rays[c + 1].direction))
			gamma = math.radians(90) - alpha
			C = scene[len(scene) // 2][0]
			size = C * (math.sin(alpha) / math.sin(gamma))
			alpha = max(ang(looking, rays[c].direction), ang(looking, rays[c + 1].direction))
			size = C * (math.sin(alpha) / math.sin(gamma)) - size
			if c == 0:
				print(alpha, gamma, C, size, scene[c][0])

		# img = pygame.transform.scale(scene[c][3], (round(25 / max(1, size - 1)) * colW, 2 * h))
		# screen.blit(img, (800 + colW * c + 1, 300 - h), (b / max(1, size), 0, colW, 2 * h))
		img = pygame.transform.scale(scene[c][3], (25 * colW, 2 * h))
		screen.blit(img, (800 + colW * c + 1, 300 - h), (b, 0, colW, 2 * h))

	pygame.draw.line(screen, (0, 255, 0), tuple(map(int, origin)),
					 tuple(map(lambda x: int(sum(x)), zip(origin, looking))), 3)
	screen.blit(font.render(str(int(clock.get_fps())), True, (0, 255, 0)), (10, 10))
	pygame.display.update()


while True:
	inp()
	loop()
	draw()
	clock.tick(120)