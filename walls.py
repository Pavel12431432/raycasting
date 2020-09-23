import pygame

bounds1 = (
	[150, 100, 100, 350],
	[150, 450, 450, 500],
	[250, 50, 450, 50],
	[500, 50, 599, 300],
	[599, 300, 450, 400],
	[200, 350, 450, 200],

	[0, 0, 600, 0],
	[600, 0, 600, 600],
	[600, 600, 0, 600],
	[0, 600, 0, 0]
)

red = (200, 50, 50)
green = (50, 200, 50)
blue = (50, 50, 200)
white = (200, 200, 200)
yellow = (200, 200, 50)
purple = (80, 20, 115)

wall_orange = pygame.image.load('wall.png')
wall_blue = pygame.image.load('wall_blue.png')

bounds2 = (
	# 1
	[125, 50, 50, 250, red],
	[50, 250, 125, 325, red],
	[125, 325, 300, 175, red],
	[300, 175, 125, 50, red],

	# 2
	[175, 350, 50, 525, yellow],
	[50, 525, 225, 475, yellow],
	[225, 475, 175, 350, yellow],

	# 3
	# [325, 350, 250, 500],
	# [250, 500, 525, 550],
	# [525, 550, 450, 400],
	# [450, 400, 325, 350],

	# 4
	[625, 450, 600, 500, white],
	[600, 500, 725, 500, white],
	[725, 500, 625, 450, white],

	# 5
	[650, 125, 575, 175, blue],
	[575, 175, 575, 325, blue],
	[575, 325, 750, 175, blue],
	[750, 175, 650, 125, blue],

	# 6
	# 20, 2, 19, 5, 31, 1, 20, 2
	[500, 50, 475, 125, purple],
	[475, 125, 775, 25, purple],
	[775, 25, 500, 50, purple],

	# edges
	[0, 0, 799, 0, green],
	[799, 0, 799, 599, green],
	[799, 599, 0, 599, green],
	[0, 599, 0, 0, green]
)

bounds3 = (
	[125, 50, 250, 50, red],
	[250, 50, 250, 150, red],
	[250, 150, 125, 150, red],
	[125, 150, 125, 50, red],

	# edges
	[0, 0, 799, 0, white],
	[799, 0, 799, 599, white],
	[799, 599, 0, 599, white],
	[0, 599, 0, 0, white]
)

bounds = (
	# 1
	[400, 400, 500, 400, green, wall_orange],
	# 2
	[500, 400, 500, 500, green, wall_orange],
	# 3
	[700, 500, 700, 600, green, wall_orange],
	# 4
	[500, 0, 500, 300, green, wall_orange],
	# 5
	[600, 100, 700, 100, green, wall_orange],
	# 6
	[600, 100, 600, 200, green, wall_orange],
	# 7
	[600, 200, 700, 200, green, wall_orange],
	# 8
	[700, 200, 700, 300, green, wall_orange],
	# 9
	[700, 300, 800, 300, green, wall_orange],
	# 10
	[600, 400, 700, 400, green, wall_orange],
	# 11
	[600, 500, 600, 300, green, wall_orange],

	# shp 1
	[100, 100, 225, 100, blue, wall_orange],
	[225, 100, 225, 125, blue, wall_orange],
	[225, 125, 175, 125, blue, wall_orange],
	[175, 125, 175, 200, blue, wall_orange],
	[175, 200, 100, 200, blue, wall_orange],
	[100, 200, 100, 100, blue, wall_orange],

	# shp 2
	[100, 300, 125, 300, red, wall_orange],
	[125, 300, 200, 400, red, wall_orange],
	[200, 400, 125, 500, red, wall_orange],
	# [125, 300, 125, 500, red],
	[125, 500, 100, 500, red, wall_orange],
	[100, 500, 100, 300, red, wall_orange],

	# edges
	[0, 0, 800, 0, white, wall_blue],
	[800, 0, 800, 600, white, wall_blue],
	[800, 600, 0, 600, white, wall_blue],
	[0, 600, 0, 0, white, wall_blue]
)