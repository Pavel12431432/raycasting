import math
import pygame
from walls import walls

player_height = 32
player_fov = 60
player_view_angle = 90
player_pos = (224, 224)
projection_plane_dimensions = (320, 200)
projection_plane_center = (projection_plane_dimensions[0] // 2, projection_plane_dimensions[1] // 2)
distance_to_projection_plane = projection_plane_center[0] / math.tan(math.radians(player_fov / 2))
angle_between_rays = player_fov / projection_plane_dimensions[0]

pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('Ray casting')
font = pygame.font.SysFont('consolas', 13)
clock = pygame.time.Clock()


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


def check_wall(grid_coordinate):
	for wall in walls:
		if wall == [grid_coordinate[0], grid_coordinate[1]]:
			return True


while True:
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (200, 50, 50), (tuple(map(lambda x: x * 64, wall)), (64, 64)))
	for i in range(8):
		pygame.draw.line(screen, (50, 50, 50), (64 * i, 0), (64 * i, 512), 2)
		pygame.draw.line(screen, (50, 50, 50), (0, 64 * i), (512, 64 * i), 2)
	angle = (player_view_angle - player_fov // 2) % 360
	for column in range(projection_plane_dimensions[0]):
		hits = []
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
		A[0] = player_pos[0] + (player_pos[1] - A[1]) / math.tan(math.radians(angle))
		A[0], A[1] = min(max(A[0], -10000), 10000), min(max(A[1], -10000), 10000)
		grid_coordinate_A = A[0] // 64, A[1] // 64
		pygame.draw.circle(screen, (50, 200, 50), (int(min(A[0], 10000)), int(min(A[1], 10000))), 2)
		if check_wall(grid_coordinate_A):
			hits.append(A)
		else:
			offset[0] = - offset[1] / math.tan(math.radians(angle))
			for i in range(1, 10):
				point = [min(max(A[0] + offset[0] * i, -10000), 10000), min(max(A[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				pygame.draw.circle(screen, (50, 200, 50), (int(point[0]), int(point[1])), 2)
				if check_wall(grid_coordinate_point):
					hits.append(point)
					break

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
		pygame.draw.circle(screen, (200, 50, 50), (int(B[0]), int(B[1])), 2)
		if check_wall(grid_coordinate_B):
			hits.append(B)
		else:
			offset[1] = -offset[0] * math.tan(math.radians(angle))
			for i in range(1, 10):
				point = [min(max(B[0] + offset[0] * i, -10000), 10000), min(max(B[1] + offset[1] * i, -10000), 10000)]
				grid_coordinate_point = point[0] // 64, point[1] // 64
				pygame.draw.circle(screen, (200, 50, 50), (int(point[0]), int(point[1])), 2)
				if check_wall(grid_coordinate_point):
					hits.append(point)
					break

		if hits:
			dist = None
			if len(hits) == 1:
				dist = math.sqrt((hits[0][0] - player_pos[0]) ** 2 + (hits[0][1] - player_pos[1]) ** 2)
				pygame.draw.rect(screen, (200, 200, 50), ((hits[0][0] // 64 * 64 + 2, hits[0][1] // 64 * 64 + 2), (62, 62)))
				pygame.draw.line(screen, (255, 255, 255), player_pos, hits[0])
			else:
				closest = min(*hits, key=lambda x: (x[0] - player_pos[0]) ** 2 + (x[1] - player_pos[1]) ** 2)
				dist = math.sqrt((closest[0] - player_pos[0]) ** 2 + (closest[1] - player_pos[1]) ** 2)
				pygame.draw.rect(screen, (200, 50, 200), ((closest[0] // 64 * 64 + 2, closest[1] // 64 * 64 + 2), (62, 62)))
				pygame.draw.line(screen, (255, 255, 255), player_pos, closest)

			beta = player_view_angle - angle
			height = 64 / dist * distance_to_projection_plane / math.cos(math.radians(beta))
			# height = round(min(max(32 / dist * distance_to_projection_plane, 0), 100)) * math.cos(math.radians(beta))
			# pygame.draw.rect(screen, (200, 200, 200), ((column, 100 - height // 2), (1, height)))
		angle += angle_between_rays

	text = font.render(str(int(clock.get_fps())), True, (200, 200, 200))
	text_rect = text.get_rect(topleft=(10, 10))
	screen.blit(text, text_rect)
	player_view_angle += 0.05
	pygame.draw.circle(screen, (50, 200, 50), player_pos, 5)
	pygame.display.update()
	inp()
	clock.tick(0)