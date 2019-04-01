from random import uniform


def sim(obs, num_iters, v_max, p):
	"""
	Returns an num_iters-by-L observation array.

	Parameters
	----------
	obs: NumPy array
		Observation array comprising the initial state.
	num_iters: int
		Number of iterations.
	v_max: int
		Maximum velocity.
	P: flt
		Probability modeling erratic driver behavior.
	"""

	L = len(obs[0])

	for n in range(num_iters):
		prev, curr = obs[-1], [-1] * L

		for i in range(L):
			if prev[i] > -1:
				v_i = prev[i]

				# The gap to the preceding vehicle
				gap = 1
				while prev[(i + gap) % L] < 0:
					gap += 1

				# Maximize velocity, but don't move further than the preceding vehicle
				v_temp = min(v_i + 1, v_max, gap - 1)
				# With probability p hit the brake, otherwise remain velocity
				v = max(v_temp - 1, 0) if uniform(0, 1) < p else v_temp
				# Perform the move
				curr[(i + v) % L] = v

		obs.append(curr)

	return obs