import math
import pygame
from walls import walls
from datetime import datetime

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

player_height = 32
block_height = 64
player_fov = 60
player_view_angle = 60
delta = datetime.now()
player_pos = (352, 352)
projection_plane_dimensions = (800, 600)
projection_plane_center_y = projection_plane_dimensions[1] // 2
distance_to_projection_plane = projection_plane_dimensions[0] // 2 / math.tan(math.radians(player_fov / 2))
angle_between_rays = player_fov / projection_plane_dimensions[0]
rotation_speed = 1.5
z_rotation_speed = 3
vertical_speed = 0.5
movement_speed = 5
grid_size = (32, 32)

pygame.init()
screen = pygame.display.set_mode(projection_plane_dimensions)
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 13)
clock = pygame.time.Clock()

bricks_img = pygame.image.load('tiles/tile' + str(6).zfill(2) + '.png').convert()
floor_img = pygame.image.load('floortile.png').convert()
ceiling_img = pygame.image.load('floortile.png').convert()

# precompute images to save time during rendering
wall_imgs = [pygame.transform.scale(bricks_img, (64, i)) for i in range(2001)]

floor_imgs = [pygame.transform.scale(floor_img, (i, 64)) for i in range(2001)]

grid = [[False] * grid_size[1] for _ in range(grid_size[0])]
for wall in walls:
	grid[wall[0]][wall[1]] = True


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
		player_view_angle -= rotation_speed * timedelta
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		player_view_angle += rotation_speed * timedelta

	if pygame.key.get_pressed()[pygame.K_DOWN]:
		projection_plane_center_y -= z_rotation_speed * timedelta
	if pygame.key.get_pressed()[pygame.K_UP]:
		projection_plane_center_y += z_rotation_speed * timedelta

	if pygame.key.get_pressed()[pygame.K_e]:
		player_height = max(min(player_height + vertical_speed * timedelta, 63), 1)
	if pygame.key.get_pressed()[pygame.K_c]:
		player_height = max(min(player_height - vertical_speed * timedelta, 63), 1)

	nextPos = player_pos
	direction = pygame.math.Vector2()
	direction.from_polar((movement_speed * timedelta, player_view_angle))
	direction.y = - direction.y
	if pygame.key.get_pressed()[ord('w')]:
		nextPos = tuple(map(sum, zip(nextPos, direction)))
	if pygame.key.get_pressed()[ord('s')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(180))))
	if pygame.key.get_pressed()[ord('a')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(90))))
	if pygame.key.get_pressed()[ord('d')]:
		nextPos = tuple(map(sum, zip(nextPos, direction.rotate(270))))
	player_pos = min(max(nextPos[0], 65), 2048 - 65), min(max(nextPos[1], 65), 2048 - 65)
	delta = datetime.now()


def check_wall(grid_coordinate):
	try:
		return grid[int(grid_coordinate[1])][int(grid_coordinate[0])]
	except IndexError:
		return False


def calculate_distance(point_a, point_b):
	try:
		return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2
	except (IndexError, TypeError):
		return float('inf')


while True:
	screen.fill((0, 0, 0))

	angle = (player_view_angle - player_fov // 2) % 360

	for column in range(projection_plane_dimensions[0]):
		tan_angle = math.tan(max(math.radians(angle), 0.00001))  # calculate tan(angle) and escape division by 0
		closest = []
		hit_horizontal, hit_vertical = None, None
		bitmap_offset = None
		# check horizontal intersection
		# find A's position
		A = [None, None]
		offset = [None, None]
		if angle <= 180:
			A[1] = player_pos[1] // 64 * 64 - 0.0000001
			offset[1] = -64
		else:
			A[1] = player_pos[1] // 64 * 64 + 64
			offset[1] = 64

		A[0] = player_pos[0] + (player_pos[1] - A[1]) / tan_angle

		A = tuple(map(lambda x: min(max(x, -10000), 10000), A))
		grid_coordinate_A = tuple(map(lambda x: x // 64, A))
		if check_wall(grid_coordinate_A):
			hit_horizontal = A
		else:
			offset[0] = - offset[1] / tan_angle
			for i in range(1, 30):
				point = [min(max(A[0] + offset[0] * i, -10000), 10000), min(max(A[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				if check_wall(grid_coordinate_point) or not (0 < point[0] < 2048 and 0 < point[1] < 2048):
					hit_horizontal = point
					break

		# check vertical intersections
		# find B's position
		B = [None, None]
		offset = [None, None]
		if not 90 < angle < 270:
			B[0] = player_pos[0] // 64 * 64 + 64
			offset[0] = 64
		else:
			B[0] = player_pos[0] // 64 * 64 - 0.0000001
			offset[0] = -64

		B[1] = player_pos[1] + (player_pos[0] - B[0]) * tan_angle
		grid_coordinate_B = B[0] // 64, B[1] // 64
		if check_wall(grid_coordinate_B):
			if calculate_distance(player_pos, B) < calculate_distance(player_pos, closest):
				hit_vertical = B
		else:
			offset[1] = -offset[0] * tan_angle
			for i in range(1, 30):
				point = [min(max(B[0] + offset[0] * i, -10000), 10000), min(max(B[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				if check_wall(grid_coordinate_point) or not (0 < point[0] < 2048 and 0 < point[1] < 2048):
					hit_vertical = point
					break

		if hit_horizontal or hit_vertical:
			if min(hit_vertical, hit_horizontal, key=lambda x: calculate_distance(x, player_pos)) == hit_vertical:
				closest = hit_vertical
				bitmap_offset = hit_vertical[1] % 64
			elif min(hit_vertical, hit_horizontal, key=lambda x: calculate_distance(x, player_pos)) == hit_horizontal:
				closest = hit_horizontal
				bitmap_offset = hit_horizontal[0] % 64

			# draw column
			beta = (player_view_angle - angle) % 360
			dist = math.sqrt(calculate_distance(closest, player_pos)) * math.cos(math.radians(beta))

			ratio = distance_to_projection_plane / dist
			scale = min(distance_to_projection_plane * 64 / dist, 2000)
			bottom_of_wall = int(ratio * player_height + projection_plane_center_y)
			top_of_wall = bottom_of_wall - scale

			# pygame.draw.circle(screen, (255, 255, 255), (column, bottom_of_wall), 1)
			# pygame.draw.line(screen, (255, 255, 255), (int(player_pos[1] // 16), int(player_pos[0] // 16)), (int(closest[1] // 16), int(closest[0] // 16)))
			pygame.draw.line(screen, (200, 200, 200), (column, top_of_wall), (column, bottom_of_wall))
			# screen.blit(wall_imgs[int(scale)], (column, top_of_wall), (bitmap_offset, 0, 1, scale))

		# if not column % 1:
		#
		# 	sin_angle = math.sin(math.radians(angle))
		# 	cos_angle = math.cos(math.radians(angle))
		# 	cos_diff = math.cos(math.radians(angle - player_view_angle))
		#
		# 	# floor casting
		# 	last_bottom_of_wall = int(bottom_of_wall)
		# 	for row in range(last_bottom_of_wall, projection_plane_dimensions[1], 1):
		# 		ratio = player_height / (row - projection_plane_center_y)
		# 		diagonal_distance = distance_to_projection_plane * ratio / cos_diff
		# 		end = [diagonal_distance * sin_angle, diagonal_distance * cos_angle]
		# 		end[0] -= player_pos[1]
		# 		end[1] += player_pos[0]
		# 		cell = int(end[0] // 64), int(end[1] // 64)
		# 		tile_row = end[1] % 64
		# 		tile_col = end[0] % 64
		# 		screen.blit(floor_img, (column, row), (tile_col, tile_row, 1, 1))
		#
		# 	# ceiling casting
		# 	last_top_of_wall = int(top_of_wall)
		# 	for row in range(last_top_of_wall, 0, -1):
		# 		ratio = (64 - player_height) / (row - projection_plane_center_y)
		# 		diagonal_distance = distance_to_projection_plane * ratio / cos_diff
		# 		end = [diagonal_distance * sin_angle, diagonal_distance * cos_angle]
		# 		end[0] += player_pos[1]
		# 		end[1] -= player_pos[0]
		# 		cell = int(end[0] // 64), int(end[1] // 64)
		# 		tile_row = end[1] % 64
		# 		tile_col = end[0] % 64
		# 		screen.blit(ceiling_img, (column, row), (tile_col, tile_row, 1, 1))

		angle = (angle + angle_between_rays) % 360

	shrunk_player_pos = int(player_pos[1] // 16), int(player_pos[0] // 16)
	pygame.draw.circle(screen, (50, 200, 50), shrunk_player_pos, 4)
	for wall in walls:
		pygame.draw.rect(screen, (200, 50, 50), ((wall[0] * 4, wall[1] * 4), (4, 4)))
	direction = pygame.math.Vector2()
	direction.from_polar((10, player_view_angle))
	pygame.draw.line(screen, (50, 200, 50), shrunk_player_pos,
					 tuple(map(lambda x: int(sum(x)), zip(direction.rotate(90), shrunk_player_pos))), 3)



	text = font.render(str(int(clock.get_fps())), True, (50, 250, 50))
	text_rect = text.get_rect(topleft=(10, 10))
	screen.blit(text, text_rect)
	pygame.display.flip()
	inp()
	clock.tick(0)