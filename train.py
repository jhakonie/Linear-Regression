import sys
import matplotlib.pyplot as plt # used for plotting the values
import my_class as my
# muista poistaa
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
	# divide the sum with the numter of values
	denormed_t0 /= xs.size
	return (denormed_t0, denormed_t1)

def normalize_list(data):
	max_x = max(data)
	min_x = min(data)
	xs = [(i - min_x) / (max_x - min_x) for i in data]
	return (xs)

def train_model(data, learning_rate):
	iterations = 2000
	losses = []
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
	for i in range(iterations):
		# predict values (price)
		y_preds = regression.predict(xs)
		# update thetas
		regression.update_t(learning_rate)
	coefs = (regression.t[0], regression.t[1])
	# convert list of values to my array type
	xs_before_normalize = my.arr(xs_before_normalize)
	ys_before_normalize = my.arr(ys_before_normalize)
	# denormalize coefficients before returning them
	coefs = denormalize_coefs(xs_before_normalize, ys_before_normalize, coefs)
	print(coefs)
	return (coefs)

# def estimate_coef(x, y):
# 	# number of observations/points
# 	n = np.size(x)
# 	# mean of x and y vector
# 	m_x = np.mean(x)
# 	m_y = np.mean(y)
# 	# calculating cross-deviation and deviation about x	
# 	SS_xy = np.sum(y*x) - n*m_y*m_x
# 	SS_xx = np.sum(x*x) - n*m_x*m_x
# 	# calculating regression coefficients
# 	b_1 = SS_xy / SS_xx
# 	b_0 = m_y - b_1*m_x
# 	print("b0 is:" + str(b_0))
# 	print("b1 is:" + str(b_1))
# 	print("========================================")
# 	return (b_0, b_1)

def plot_regression_line(x, y, t):
	# plotting the data points
	plt.scatter(x, y, color = "b", marker = "o", s = 30)
	# predicted y-values
	y_pred = t[0] + t[1] * x
	# plotting the regression line
	plt.plot(x, y_pred, color = "g")
	# putting labels
	plt.xlabel('x')
	plt.ylabel('y')
	# function to show plot
	plt.show()

# create a file "coefs.csv" and write the learned thetas there
def save_coefs_to_file(coefs):
	fd = open("coefs.csv", "w")
	fd.close()
	fd = open("coefs.csv", "a")
	fd.write("t0,t1\n")
	fd.write(str(coefs[0])+","+str(coefs[1]))
	fd.close()

# def test_with_numpy(data):
# 	xs = np.array([float(i[0]) for i in data])
# 	ys = np.array([float(i[1]) for i in data])
# 	b = estimate_coef(xs, ys)
# 	# plot_regression_line(xs, ys, b)
# 	max_x = max(xs)
# 	min_x = min(xs)
# 	max_y = max(ys)
# 	min_y = min(ys)
# 	test_ys = ys
# 	test_xs = xs
# 	x_max_interval = max_x - min_x
# 	y_max_interval = max_y - min_y
# 	xs = np.array([(i - min_x) / (max_x - min_x) for i in xs])
# 	ys = np.array([(i - min_y) / (max_y - min_y) for i in ys])
# 	b = train_model(data, 0.0001)
# 	denormed_b1 = b[1] * y_max_interval / x_max_interval
# 	save_coefs_to_file(b)
# 	denormed_b0 = np.sum(test_ys - (test_xs * denormed_b1)) / np.size(xs)
# 	# # y = kx + b
# 	# calc_y_when_x_is_1 = 
# 	print("b0 is:" + str(denormed_b0))#b[0]))
# 	print("b1 is:" + str(b[1] * y_max_interval / x_max_interval))
# 	# print("b0 is:" + str(b[0]))
# 	# print("b1 is:" + str(b[1]))
# 	# 
# 	# plot_regression_line(xs, ys, b)
# 	return

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
		# use matplot to visualize data and prediction line
		plot_regression_line(xs, ys, coefs)
	else:
		print("give the path to a csv file as argument")

main()
