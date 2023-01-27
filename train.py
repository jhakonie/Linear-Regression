import sys
import matplotlib.pyplot as plt # used for plotting the values
import my_class as my
import numpy as np # used for plotting the values, matplot requires numpy-arrays

def denormalize_coefs(xs, ys, coefs):
	max_x = max(xs.array)
	min_x = min(xs.array)
	max_y = max(ys.array)
	min_y = min(ys.array)
	x_diff = max_x - min_x
	y_diff = max_y - min_y
	denormed_t1 = coefs[1] * y_diff / x_diff
	#
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

def normalize_list(data):
	max_x = max(data)
	min_x = min(data)
	xs = [(i - min_x) / (max_x - min_x) for i in data]
	return (xs)

def train_model(data, learning_rate):
	losses = []
	iteration = 0
	# mileage
	xs_before_normalize = [float(i[0]) for i in data]
	# price
	ys_before_normalize = [float(i[1]) for i in data]
	# normalize data
	xs = normalize_list(xs_before_normalize)
	ys = normalize_list(ys_before_normalize)
	learning_rate = 0.1
	# declare the linear regression class
	regression = my.linear_regression(xs, ys)
	# Train the model with gradient decent:
	# iterate the regression until it is accurate enough
	while (1):
		# predict values (price)
		y_preds = regression.predict(xs)
		# update thetas
		regression.update_t(learning_rate)
		# calculate loss with mean squre error
		loss = regression.calculate_loss(y_preds)
		losses.append(loss)
		if (iteration > 0 and abs(losses[iteration - 1] - losses[iteration]) < 0.0000000001):
			break
		iteration += 1
	coefs = (regression.t[0], regression.t[1])
	# convert list of values to my array type
	xs_before_normalize = my.arr(xs_before_normalize)
	ys_before_normalize = my.arr(ys_before_normalize)
	# denormalize coefficients using the pre-normalized data
	coefs = denormalize_coefs(xs_before_normalize, ys_before_normalize, coefs)
	return (coefs)

# create a file "coefs.csv" and write the learned thetas there
def save_coefs_to_file(coefs):
	fd = open("coefs.csv", "w")
	fd.close()
	fd = open("coefs.csv", "a")
	fd.write("t0,t1\n")
	fd.write(str(coefs[0])+","+str(coefs[1]))
	fd.close()

def plot_regression_line(x, y, t, color_string, style_string):
	# plotting the data points
	plt.scatter(x, y, color = "b", marker = "o", s = 30)
	# predicted y-values
	y_pred = t[0] + t[1] * x
	# plotting the regression line
	plt.plot(x, y_pred, color = color_string, linestyle = style_string)
	# putting labels
	plt.xlabel('x')
	plt.ylabel('y')

# The math that actually calculates the result, just for comparison.
def estimate_coef(x, y):
	# number of observations/points
	n = np.size(x)
	# mean of x and y vector
	m_x = np.mean(x)
	m_y = np.mean(y)
	# calculating cross-deviation and deviation about x
	SS_xy = np.sum(y*x) - n*m_y*m_x
	SS_xx = np.sum(x*x) - n*m_x*m_x
	# calculating regression coefficients
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1*m_x
	return (b_0, b_1)

def main():
	if (len(sys.argv) == 2):
		file_name = sys.argv[1]
		# read the csv-file to an array
		data = my.read_csv_to_list(file_name)
		coefs = train_model(data, 0.1)
		save_coefs_to_file(coefs)
		# use numpy arrays to be able to use matplot for data visualisation
		xs = np.array([float(i[0]) for i in data])
		ys = np.array([float(i[1]) for i in data])
		# Use another function to mathematically calculate the coeffs
		coefs_math = estimate_coef(xs, ys)
		# use matplot to visualize data, the prediction line and the calculated line
		plot_regression_line(xs, ys, coefs_math, "r", "solid")
		plot_regression_line(xs, ys, coefs, "g", "dotted")
		plt.show()
	else:
		print("give the path to a csv file as argument")

main()
