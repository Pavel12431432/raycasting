import pygame

SCREEN_SIZE = 600, 500
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
SURFACE = pygame.image.load('walls/wall_green.png')
SURFACE = pygame.transform.scale2x(pygame.transform.scale2x(SURFACE))

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()

	SCREEN.blit(SURFACE, (200 - 25, 300), (0, 50, 65, 100))
	pygame.draw.circle(SCREEN, (255, 255, 255), (200, 300), 3)
	pygame.display.flip()
	CLOCK.tick(30)