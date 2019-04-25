from generator import *
from simulator import sim
import argparse


#######################################################################
# This part plots the change of traffic flow along with the timesteps #
#######################################################################


def main(args):
	init = init_state(L=args.L)
	obs = sim(obs=init, num_iters=args.num_iters, v_max=args.v_max, p=args.p)

	# Display the results
	disp = np.zeros(shape=(args.num_iters, args.L))
	for i in range(args.num_iters):
		for j in range(args.L):
			disp[i][j] = 1 if obs[i][j] > -1 else 0

	plt.imshow(disp, cmap="Greys", interpolation="nearest")
	plt.gca().invert_yaxis()
	plt.ylabel("Timestep")
	plt.xlabel("Flow")
	plt.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run_file')
	parser.add_argument('--L', type=int, default=500)
	parser.add_argument('--num_iters', type=int, default=500)
	parser.add_argument('--v_max', type=int, default=5)
	parser.add_argument('--p', type=float, default=0.2)
	args = parser.parse_args()
	main(args)