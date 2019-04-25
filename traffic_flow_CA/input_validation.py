from generator import *
from random import randrange
import argparse


#########################################################################
# This part is for input validation based on the empirical distribution #
#########################################################################


def ReservoirSample(src, k):
	'''
	Randomly chooses k elements from the source list with Reservoir Sampling algorithm.
	Returns a list with all the chosen elements.

	Parameters
	----------
	src: List
		A list comprising the whole elements.
	k: int
		The number of elements needed to choose.
	'''
	N = len(src)  # The total number of elements in the original list

	reservoir = []
	for i in range(k):
		reservoir.append(src[i])

	i = 0
	while i < N:
		j = randrange(i + 1)
		if j < k:
			reservoir[j] = src[i]
		i += 1

	return reservoir



def validation(input_file, test):
	'''
	Calculates the accuracy of empirical distribution.
	Returns the accuracy percentage.

	Parameters
	----------
	input_file: str
		The name of input data file.
	test: float
		The percentage of data for testing set.
		Should be in the range of (0, 1)
	'''
	src = cleaning(input_file)

	# Seperate the training set and testing set
	k = int(test * len(src))
	test_set = ReservoirSample(src=src, k=k)

	to_train = src
	for num in test_set:
		to_train.remove(num)
	train_set = to_train

	# Generate empirical distribution using training set
	x_train, y_train = ecdf(time_table=train_set)

	# Generate empirical distribution using testing set
	N = len(test_set)
	cdfx = sorted(test_set)

	inter = np.zeros((N - 1, 1))
	for i in range(N - 1):
		inter[i][0] = cdfx[i + 1] - cdfx[i]

	x_test = list(np.linspace(start=min(inter), stop=max(inter), num=N - 1))
	y_test = []

	for x in x_test:
		temp = inter[inter <= x]
		y = temp.size / (N - 1)
		y_test.append(y)

	# Plot the results for comparison
	plt.plot(x_train, y_train, label='training_set')
	plt.plot(x_test, y_test, label='testing_set')
	plt.legend()
	plt.show()



def main(args):
	validation(input_file='input.csv', test=args.test)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run_file')
	parser.add_argument('--test', type=float, default=0.2)
	args = parser.parse_args()
	main(args)