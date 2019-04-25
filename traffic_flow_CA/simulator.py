from generator import *
import statistics
import argparse


"""
References
----------
Rickert, Marcus, et al. "Two lane traffic simulations using cellular automata." 
Physica A: Statistical Mechanics and its Applications 231.4 (1996): 534-550.
"""


################################################################
# This part calculates the average in-system time of a vehicle #
###############################################################


def sim(obs, num_iters, v_max, p):
	'''
	Returns an num_iters-by-L observation array.

	Parameters
	----------
	obs: NumPy array
		Observation array comprising the initial state.
	num_iters: int
		Number of iterations.
	v_max: int
		Maximum velocity.
	p: float
		Probability modeling erratic driver behavior.
	'''
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


def timer(obs):
	'''
	Returns the average timesteps spent for each car to pass the system.

	Parameters
	----------
	obs: List[List[int]]
		A 2-dimensional array consisting of observations.
	'''
	queue = obs[0]
	L = len(queue)

	pass_time = []
	# Get the starting location for each vehicle
	init_loc = [i for i in range(L) if queue[i] > -1]
	for temp_loc in init_loc:

		# Record the timesteps used for passing the system for each vehicle
		prev, curr = 0, 1
		while obs[prev][temp_loc] + temp_loc < L and curr < len(obs):
			if obs[curr][obs[prev][temp_loc] + temp_loc] >= 0:
				temp_loc += obs[prev][temp_loc]
			prev += 1
			curr += 1
		pass_time.append(prev)

	return statistics.mean(pass_time)



def main(args):
	output = []
	for k in range(args.num_sim):
		init = init_state(L=args.L)
		obs = sim(obs=init, num_iters=args.num_iters, v_max=args.v_max, p=args.p)
		avg_time = timer(obs=obs)
		output.append(avg_time)
		print('Sim No. %d: average timesteps in the system:' % k, avg_time)
	print(statistics.mean(output))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run_file')
	parser.add_argument('--num_sim', type=int, default=200)
	parser.add_argument('--L', type=int, default=500)
	parser.add_argument('--num_iters', type=int, default=500)
	parser.add_argument('--v_max', type=int, default=5)
	parser.add_argument('--p', type=float, default=0.2)
	args = parser.parse_args()
	main(args)