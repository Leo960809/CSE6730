import pandas as pd
import numpy as np
import scipy.stats as sp
import math
from random import uniform
import matplotlib.pyplot as plt


#########################################################################################
# This part generates the empirical distribution and sets up the random input generator #
#########################################################################################


def cleaning(input_file):
	'''
	Based on the source data, filters all the vehicles that pass all five intersections.
	Returns an 1-by-N NumPy array consisting of the arrival time of cars.

	Parameters
	----------
	input_file: str
		The name of input data file.
	'''
	data = pd.read_csv(input_file)
	data_1 = data[data['Intersection'] != 0].drop_duplicates(subset=['Vehicle_ID', 'Intersection'], keep='first')

	grouped = data_1.groupby(by=['Vehicle_ID'])
	grouped.filter(lambda x: len(x) == 5).to_csv('grouped.csv')

	src = pd.read_csv('grouped.csv')
	src_1 = src[src['Intersection'] == 1]
	time = src_1[['Epoch_ms']].get_values()

	out = []
	for i in range(len(time)):
		out.append(time[i][0])

	return out


def ecdf(time_table):
	'''
	Generates the empirical distribution based on the interarrival time.
	Returns a tuple (x, y) representing its Cumulative Distribution Function.

	Parameters
	----------
	time_table: List
		A list representing the attribute of each car.
	'''
	N = len(time_table)
	cdfx = sorted(time_table)

	inter = np.zeros((N - 1, 1))
	for i in range(N - 1):
		inter[i][0] = cdfx[i + 1] - cdfx[i]

	x_values = list(np.linspace(start=min(inter), stop=max(inter), num=N - 1))
	y_values = []

	for x in x_values:
		temp = inter[inter <= x]
		y = temp.size / (N - 1)
		y_values.append(y)

	########################################################
	# Plot the normal cumulative distribution for comparison
	#mu = sum(inter) / (N - 1)
	#sigma = math.sqrt(1 / (N - 2) * sum((inter - mu) ** 2))
	#func_norm = sp.norm.cdf(x_values, loc=mu, scale=sigma)

	#plt.plot(x_values, func_norm, label='ncdf')
	#plt.plot(x_values, y_values, label='ecdf')
	#plt.legend()
	#plt.show()
	#########################################################

	return x_values, y_values


def generator(x, y):
	'''
	Random generator of interarrival time based on the empirical distribution.
	Returns an integer with the unit of second

	Parameters
	----------
	x: list
		List containing the interarrival time.
	y: list
		List containing the corresponding cumulative probability.
	'''
	rand = uniform(0, 1)
	ret = x[y.index(min(y, key=lambda t: abs(t - rand)))]

	return ret / 1000


def init_state(L):
	'''
	Returns an 1-by-L array representing the initial state of the traffic flow,
	which is randomly generated according to the empirical distribution.

	Parameters
	----------
	L: int
		Number of cells in total.
	'''
	x_values, y_values = ecdf(time_table=cleaning('input.csv'))
	initial = [-1] * L

	# Consider the first vehicle
	rand_time = int(generator(x=x_values, y=y_values))
	if rand_time == 0:
		initial[0] = 0

	# Consider the following vehicles
	time_table = []
	temp = 1
	while temp < L:
		time_table.append(temp)
		inter_time = int(generator(x=x_values, y=y_values))
		temp += inter_time

	for i in range(1, L):
		if i in time_table:
			initial[i] = 0

	obs = [initial]

	return obs