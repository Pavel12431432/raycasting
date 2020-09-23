class Ray:
	def __init__(self, x, y, direction):
		self.pos = (x, y)
		self.direction = direction
		self.closest = None

	# noinspection PyTupleAssignmentBalance
	def cast(self, wall):
		x1, y1, x2, y2 = *wall.a, *wall.b
		x3, y3, x4, y4 = *self.pos, *map(sum, zip(self.pos, self.direction))

		if (den := (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) == 0:
			return

		t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
		u = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

		if 1 >= t >= 0 >= u:
			x = int(x1 + t * (x2 - x1))
			y = int(y1 + t * (y2 - y1))
			return x, y, u
