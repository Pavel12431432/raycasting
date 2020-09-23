import pygame


class Wall:
	def __init__(self, x1, y1, x2, y2, color):
		self.a = (x1, y1)
		self.b = (x2, y2)
		self.color = color

	def show(self, screen):
		pygame.draw.line(screen, (255, 0, 0), self.a, self.b, 1)
