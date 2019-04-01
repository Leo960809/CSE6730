from random import shuffle


def init_state(L, density):
	"""
	Returns an 1-by-L array representing the initial state of the traffic flow,
	which is randomly generated according to the given density.

	Parameters
	----------
	L: int
		Number of cells in total.
	density: flt
		Density of vehicles.
	"""
	cars_num = int(density * L)
	initial = [0] * cars_num + [-1] * (L - cars_num)
	shuffle(initial)
	obs = [initial]

	return obs