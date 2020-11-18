import math
import pygame
from walls import walls
from random import randint
from datetime import datetime

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

player_height = 32
block_height = 64
player_fov = 60
player_view_angle = 90
delta = datetime.now()
player_pos = (224, 224)
projection_plane_dimensions = (320, 200)
projection_plane_center_y = projection_plane_dimensions[1] // 2
distance_to_projection_plane = projection_plane_dimensions[0] // 2 / math.tan(math.radians(player_fov / 2))
angle_between_rays = player_fov / projection_plane_dimensions[0]

pygame.init()
screen = pygame.display.set_mode(projection_plane_dimensions)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 13)
clock = pygame.time.Clock()

bricks_img = pygame.image.load('tiles/tile' + str(7).zfill(2) + '.png').convert()
floor_img = pygame.image.load('floortile.png').convert()
ceiling_img = pygame.image.load('floortile.png').convert()

# precompute images to save time during rendering
wall_imgs = [pygame.transform.scale(bricks_img, (64, i)) for i in range(projection_plane_dimensions[1] * 10 + 1)]


def inp():
	global player_pos, player_view_angle, delta, projection_plane_center_y, player_height
	if not (timedelta := abs(delta - datetime.now()).microseconds / 16666.66):
		timedelta = 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
			quit()

	if not sum(pygame.key.get_pressed()):
		delta = datetime.now()
		return

	if pygame.key.get_pressed()[pygame.K_LEFT]:
		player_view_angle -= 1.5 * timedelta
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		player_view_angle += 1.5 * timedelta

	if pygame.key.get_pressed()[pygame.K_DOWN]:
		projection_plane_center_y -= 3 * timedelta
	if pygame.key.get_pressed()[pygame.K_UP]:
		projection_plane_center_y += 3 * timedelta

	if pygame.key.get_pressed()[pygame.K_e]:
		player_height = max(min(player_height + .5 * timedelta, 64), 0)
	if pygame.key.get_pressed()[pygame.K_c]:
		player_height = max(min(player_height - .5 * timedelta, 64), 0)

	nextPos = player_pos
	direction = pygame.math.Vector2()
	direction.from_polar((2 * timedelta, player_view_angle))
	direction.y = - direction.y
	if pygame.key.get_pressed()[ord('w')]:
		nextPos = tuple(map(sum, zip(nextPos, direction)))
	if pygame.key.get_pressed()[ord('s')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(180))))
	if pygame.key.get_pressed()[ord('a')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(90))))
	if pygame.key.get_pressed()[ord('d')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(270))))
	player_pos = min(max(nextPos[0], 65), 448), min(max(nextPos[1], 65), 448)
	delta = datetime.now()


def check_wall(grid_coordinate):
	for wall in walls:
		if wall == [grid_coordinate[0], grid_coordinate[1]]:
			return True


def calulate_distance(point_a, point_b):
	try:
		return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2
	except IndexError:
		return float('inf')


while True:
	screen.fill((0, 0, 0))
	angle = (player_view_angle - player_fov // 2) % 360
	for column in range(projection_plane_dimensions[0]):
		closest = []
		bitmap_offset = None
		# check horizontal intersection
		# find A's position
		A = [None, None]
		offset = [None, None]
		if angle < 180:
			A[1] = player_pos[1] // 64 * 64 - 1
			offset[1] = -64
		else:
			A[1] = player_pos[1] // 64 * 64 + 64
			offset[1] = 64
		if math.radians(angle):
			A[0] = player_pos[0] + (player_pos[1] - A[1]) / math.tan(math.radians(angle))
		else:
			A[0] = 10000
		A[0], A[1] = min(max(A[0], -10000), 10000), min(max(A[1], -10000), 10000)
		grid_coordinate_A = A[0] // 64, A[1] // 64
		if check_wall(grid_coordinate_A):
			closest = A
		else:
			if math.radians(angle):
				offset[0] = - offset[1] / math.tan(math.radians(angle))
			else:
				offset[0] = 10000
			for i in range(1, 10):
				point = [min(max(A[0] + offset[0] * i, -10000), 10000), min(max(A[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				if check_wall(grid_coordinate_point):
					closest = point
					break

		if closest:
			bitmap_offset = closest[0] % 64

		# check vertical intersections
		# find B's position
		B = [None, None]
		offset = [None, None]
		if not 90 < angle < 270:
			B[0] = player_pos[0] // 64 * 64 + 64
			offset[0] = 64
		else:
			B[0] = player_pos[0] // 64 * 64 - 1
			offset[0] = -64

		B[1] = player_pos[1] + (player_pos[0] - B[0]) * math.tan(math.radians(angle))
		grid_coordinate_B = B[0] // 64, B[1] // 64
		if check_wall(grid_coordinate_B):
			if calulate_distance(player_pos, B) < calulate_distance(player_pos, closest):
				closest = B
		else:
			offset[1] = -offset[0] * math.tan(math.radians(angle))
			for i in range(1, 10):
				point = [min(max(B[0] + offset[0] * i, -10000), 10000), min(max(B[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				if check_wall(grid_coordinate_point):
					if calulate_distance(player_pos, point) < calulate_distance(player_pos, closest):
						closest = point
					break

		if closest and bitmap_offset is None:
			bitmap_offset = closest[1] % 64
		elif closest and bitmap_offset and not closest[0] % 64 == bitmap_offset:
			bitmap_offset = closest[1] % 64

		if closest:
			# draw column
			beta = (player_view_angle - angle) % 360
			dist = math.sqrt(calulate_distance(closest, player_pos)) * math.cos(math.radians(beta))

			ratio = distance_to_projection_plane / dist
			scale = distance_to_projection_plane * 64 / dist
			bottom_of_wall = ratio * player_height * 2 / 2 + projection_plane_center_y
			top_of_wall = bottom_of_wall - scale

			height = min(bottom_of_wall - top_of_wall, 2000)

			screen.blit(wall_imgs[int(min(scale, 2000))], (column, top_of_wall), (bitmap_offset, 0, 1, height))
			# floor casting
			if not column % 2:
				last_bottom_of_wall = int(bottom_of_wall)
				for row in range(last_bottom_of_wall, projection_plane_dimensions[1], 2):
					ratio = player_height / (row - projection_plane_center_y)
					diagonal_distance = distance_to_projection_plane * ratio / math.cos(
						math.radians(angle - player_view_angle))
					end = [diagonal_distance * math.sin(math.radians(angle)),
						   diagonal_distance * math.cos(math.radians(angle))]
					end[0] -= player_pos[1]
					end[1] += player_pos[0]
					cell = int(end[0] // 64), int(end[1] // 64)
					tile_row = end[1] % 64
					tile_col = end[0] % 64
					screen.blit(floor_img, (column, row), (tile_col, tile_row, 2, 2))

				# ceiling casting
				last_top_of_wall = int(top_of_wall)
				for row in range(last_top_of_wall, 0, -2):
					ratio = (64 - player_height) / (row - projection_plane_center_y)
					diagonal_distance = distance_to_projection_plane * ratio / math.cos(
						math.radians(angle - player_view_angle))
					end = [diagonal_distance * math.sin(math.radians(angle)),
						   diagonal_distance * math.cos(math.radians(angle))]
					end[0] += player_pos[1]
					end[1] -= player_pos[0]
					cell = int(end[0] // 64), int(end[1] // 64)
					tile_row = end[1] % 64
					tile_col = end[0] % 64
					screen.blit(ceiling_img, (column, row), (tile_col, tile_row, 2, 2))

		angle = (angle + angle_between_rays) % 360

	text = font.render(str(int(clock.get_fps())), True, (50, 250, 50))
	text_rect = text.get_rect(topleft=(10, 10))
	screen.blit(text, text_rect)
	pygame.display.update()
	inp()
	clock.tick(0)