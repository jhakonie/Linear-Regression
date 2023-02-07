#!/usr/bin/env python
import sys
import my_class as my
import matplotlib.pyplot as plt # used for plotting the values
import numpy as np # used for plotting the values, matplotlib requires numpy-arrays
import matplotlib.animation as animation # used to create an animation of the regression

# ------------------------------------------------------------------------------------------------------
# Some global variables to help create an animation
# ------------------------------------------------------------------------------------------------------
argument_count = len(sys.argv)
if (argument_count == 2 or argument_count == 3):
	file_name = sys.argv[1]
	# read the csv-file to an array
	data = my.read_csv_to_list(file_name)
	xs = np.array([float(i[0]) for i in data])
	ys = np.array([float(i[1]) for i in data])
	fig, ax = plt.subplots()
	x = np.arange(min(xs), max(xs), 0.5)
	t = (0, 0)
	line, = ax.plot(x, t[0] + t[1] * x)

# save coefs in a list during training to create an animation
coefs_list = []

# ------------------------------------------------------------------------------------------------------
# The math that actually calculates the analytical, "correct", result. Used just for comparison.
# ------------------------------------------------------------------------------------------------------

def estimate_coef(x, y):
	# number of observations/points
	n = np.size(x)
	# mean of x and y vector
	m_x = np.mean(x)
	m_y = np.mean(y)
	# calculating cross-deviation and deviation about x
	SS_xy = np.sum(y * x) - n * m_y * m_x
	SS_xx = np.sum(x * x) - n * m_x * m_x
	# calculating regression coefficients
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1 * m_x
	return (b_0, b_1)

# ------------------------------------------------------------------------------------------------------
# Visualisation
# ------------------------------------------------------------------------------------------------------

def plot_regression_line(x, y, t, color_string, style_string):
	# predicted y-values
	y_pred = t[0] + t[1] * x
	# plotting the regression line
	plt.plot(x, y_pred, color = color_string, linestyle = style_string)

def animate(i):
	t = coefs_list[i]
	line.set_ydata((t[0] + t[1] * x)) # update the data.
	return line,

def visualise_results(coefs):
	# use numpy arrays to be able to use matplot for data visualisation
	xs = np.array([float(i[0]) for i in data])
	ys = np.array([float(i[1]) for i in data])
	# putting labels
	plt.xlabel('mileage')
	plt.ylabel('price')
	# Use another function to mathematically calculate the coeffs
	coefs_math = estimate_coef(xs, ys)
	# use matplot to visualize data, the prediction line (g) and the calculated line (r)
	plot_regression_line(xs, ys, coefs_math, "r", "solid")
	plot_regression_line(xs, ys, coefs, "g", "dotted")
	# plotting the data points
	ani = animation.FuncAnimation(fig, animate, interval=1.0, blit=False, frames=len(coefs_list))
	plt.scatter(xs, ys, color = "m", marker = "o", s = 40)
	plt.show()

	# To save the animation
	# ani.save("movie.mp4")

# ------------------------------------------------------------------------------------------------------
# Denormalize coefficients
# ------------------------------------------------------------------------------------------------------

def denormalize_coefs(xs, ys, coefs):
	xs = xs if isinstance(xs, my.arr) else my.arr(xs)
	ys = ys if isinstance(ys, my.arr) else my.arr(ys)
	max_x = max(xs.array)
	min_x = min(xs.array)
	max_y = max(ys.array)
	min_y = min(ys.array)
	x_diff = max_x - min_x
	y_diff = max_y - min_y
	denormed_t1 = coefs[1] * y_diff / x_diff
	# y = t1 * x + t0
	# t0 = y - t1 * x
	#
	# t1 * x
	xs_multiplied_by_t1 = xs.multiply_scalar(denormed_t1)
	# y - t1 * x
	ys_minus_xs_multiplied_by_t1 = ys - xs_multiplied_by_t1
	# get the sum of the values
	denormed_t0 = ys_minus_xs_multiplied_by_t1.sum_self()
	# divide the sum with the number of values
	denormed_t0 /= xs.size
	return (denormed_t0, denormed_t1)

# ------------------------------------------------------------------------------------------------------
# Normalize the values of a list
# ------------------------------------------------------------------------------------------------------

def normalize_list(data):
	max_x = max(data)
	min_x = min(data)
	xs = [(i - min_x) / (max_x - min_x) for i in data]
	return (xs)

# ------------------------------------------------------------------------------------------------------
# Train with gradient descent
# ------------------------------------------------------------------------------------------------------

def train_model(data, plot_on):
	# initialize the list of loss values
	losses = []
	# mileage
	xs_before_normalize = [float(i[0]) for i in data]
	# price
	ys_before_normalize = [float(i[1]) for i in data]
	plot_xs = np.array([float(i[0]) for i in data])
	plot_ys = np.array([float(i[1]) for i in data])
	# normalize data
	xs = normalize_list(xs_before_normalize)
	ys = normalize_list(ys_before_normalize)
	learning_rate = 0.1
	# declare the linear regression class, see my_plass.py for definition
	regression = my.linear_regression(xs, ys)
	# Train the model with gradient descent: iterate the regression until it is accurate enough
	iteration = 0
	while (1):
		# predict values (price)
		y_preds = regression.predict(xs)
		# update thetas
		regression.update_t(learning_rate)
		# calculate loss with mean square error
		loss = regression.calculate_loss(y_preds)
		# save loss
		losses.append(loss)
		# compare to the previous loss and stop, if the difference is small enough
		if (iteration > 0 and abs(losses[iteration - 1] - losses[iteration]) < 0.00000000001):
			break
		iteration += 1
		coefs = (regression.t[0], regression.t[1])
		coefs = denormalize_coefs(xs_before_normalize, ys_before_normalize, coefs)
		# keep a list of the normalized thetas, for visualization later
		coefs_list.append(coefs)
		# plot the result with matplotlib, if the plot_on flag is on
		if (plot_on):
			plot_regression_line(plot_xs, plot_ys, coefs, "g", "dotted")
	return (coefs)

# ------------------------------------------------------------------------------------------------------
# Create a file "coefs.csv" and write the learned thetas there
# ------------------------------------------------------------------------------------------------------

def save_coefs_to_file(coefs):
	fd = open("coefs.csv", "w")
	fd.close()
	fd = open("coefs.csv", "a")
	fd.write("t0,t1\n")
	fd.write(str(coefs[0])+","+str(coefs[1]))
	fd.close()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def main():
	if (argument_count == 2 or argument_count == 3):
		if (argument_count == 2):
			plot_on = False
		else:
			plot_on = True
		coefs = train_model(data, plot_on)
		save_coefs_to_file(coefs)
		visualise_results(coefs)
	else:
		print("give the path to a csv file as argument.")

main()
