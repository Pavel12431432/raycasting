walls = [
	# outer walls
	*[(x, 0) for x in range(32)],
	*[(x, 31) for x in range(32)],
	*[(0, y) for y in range(32)],
	*[(31, y) for y in range(32)],

	# 1
	*[(6, y) for y in range(8, 5, -1)],
	*[(x, 5) for x in range(6, 1, -1)],
	*[(2, y) for y in range(4, 2, -1)],
	*[(x, 2) for x in range(2, 10)],
	*[(9, y) for y in range(3, 9)],

	# 2
	*[(16, y) for y in range(6, 9)],
	*[(x, 9) for x in range(16, 22)],
	*[(21, y) for y in range(8, 1, -1)],

	# 3 smile
	(20, 25),
	(20, 26),
	(19, 26),
	*[(x, 27) for x in range(19, 10, -1)],
	*[(x, 28) for x in range(18, 11, -1)],
	(11, 26),
	(10, 26),
	(10, 25),

	# 4
	*[(25, y) for y in range(18, 29)],
	*[(x, 28) for x in range(24, 22, -1)],

	# 1x6 (25, 6)
	*[(26, y) for y in range(5, 11)],

	# 4x1 (6, 11)
	*[(x, 11) for x in range(6, 11)],

	# 4x1 (1, 14)
	*[(x, 14) for x in range(1, 5)],

]