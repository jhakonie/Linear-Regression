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
	denormed_b1 = coefs[1] * y_diff / x_diff
	# 
	# y = b1 * x + b0
	# b0 = y - b1 * x
	# 
	# b1 * x
	xs_multiplied_by_b1 = xs.multiply_scalar(denormed_b1)
	# y - b1 * x
	ys_minus_xs_multiplied_by_b1 = ys - xs_multiplied_by_b1
	# get the sum of the values
	denormed_b0 = ys_minus_xs_multiplied_by_b1.sum_self()
	# divide the sum with the number of values
	denormed_b0 /= xs.size
	return (denormed_b0, denormed_b1)

def normalize_list(data):
	max_x = max(data)
	min_x = min(data)
	xs = [(i - min_x) / (max_x - min_x) for i in data]
	return (xs)

def train_model(data, learning_rate):
	iterations = 2000
	losses = []
	xs_before_normalize = [float(i[0]) for i in data] #mileage
	ys_before_normalize = [float(i[1]) for i in data] #price
	xs = normalize_list(xs_before_normalize)
	ys = normalize_list(ys_before_normalize)
	learning_rate = 0.1
	# declare the linear regression class
	regression = my.linear_regression(xs, ys)
	# iterate the regression until it is accurate enough
	for i in range(iterations):
		# predict
		y_preds = regression.predict(xs)
		# update thetas
		regression.update_t(learning_rate)
	coefs = (regression.t[0], regression.t[1])
	xs_before_normalize = my.arr(xs_before_normalize)
	ys_before_normalize = my.arr(ys_before_normalize)
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

# def read_data(file_name):
# 	exists = os.path.exists(file_name)
# 	# print(exists)
# 	if (exists):
# 		fd = open(file_name, "r") #todo: remember to add close fd
# 		fd = [x.strip() for x in fd]
# 		# print(fd)
# 		fd.pop(0)
# 		data = []
# 		for x in fd:
# 			values = x.split(",")
# 			data.append(values)
# 		# print(data)
# 		fd.close()
# 		return data
# 	else:
# 		print("No file found.")
# 		quit()

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
		plot_regression_line(xs, ys, coefs)
	else:
		print("give the path to a csv file as argument")

main()

# y = mx + b
# y - y0 = (x - x0)m + b
# m = (y - b) / x
# b = y - mx
