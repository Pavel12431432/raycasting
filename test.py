import pygame

img = pygame.transform.scale(pygame.image.load('tiles/tile07.png'), (64, 64))

for i in range(64):
	s = pygame.Surface((1, 64))
	s.blit(img, (-i, 0, 64, 64))
	pygame.image.save(s, 'tile7/' + str(i) + '.png')