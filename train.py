import sys
import matplotlib.pyplot as plt
import my_class as my
# muista poistaa
import numpy as np

# def tweak_learning_rate(regression, losses, y_preds, learning_rate):
# 	mean_x = regression.xs.sum_add_self() / regression.xs.size
# 	mean_y = regression.ys.sum_add_self() / regression.ys.size
# 	test_0 = regression.t[0] + 2 * regression.t[1]
# 	test_1 = regression.t[0] + 4 * regression.t[1]
# 	if (test_0 > test_1):
# 		learning_rate = (test_0 - test_1) / (2 - regression.t[0])
# 	return learning_rate


def train_model(data, learning_rate):
	iterations = 1000
	losses = []
	xs = [float(i[0]) for i in data] #mileage
	ys = [float(i[1]) for i in data] #price
	max_x = max(xs)
	min_x = min(xs)
	max_y = max(ys)
	min_y = min(ys)
	xs = [(i - min_x) / (max_x - min_x) for i in xs]
	ys = [(i - min_y) / (max_y - min_y) for i in ys]
	# print(max_x)
	# divisor = len(ys)**2 * 100
	# learning_rate = 1 / divisor
	learning_rate = 0.1
	# learning_rate = 0.00015
	# xs.reverse()
	# steps = 100 #todo remove
	regression = my.linear_regression(xs, ys)
	for i in range(iterations):
		y_preds = regression.predict(xs)
		loss = regression.calculate_loss(y_preds)
		losses.append(loss)
		# if (i > 0 and losses[i] > losses[i-1]):
		# 	learning_rate *= -1
		# learning_rate = tweak_learning_rate(regression, losses, y_preds, learning_rate)
		regression.update_t(learning_rate)
		# if (loss > 100):
		# 	learning_rate /= 10
		# 	regression = my.linear_regression(xs, ys)
			# return train_model(data, learning_rate)
		# if i % steps == 0:
		# 	print(iterations, "epochs elapsed") 
		# 	print("Current accuracy is :", 
		# 		regression.get_current_accuracy(y_preds))			
		# 	stop = input("Do you want to stop (y/*)??") 
		# 	if stop == "y": 
		# 		break

	print("________________________________________")
	print(losses)
	print("________________________________________")
	return (regression.t[0], regression.t[1])

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

def plot_regression_line(x, y, b):
	# plotting the actual points as scatter plot
	plt.scatter(x, y, color = "m", marker = "o", s = 30)
	# predicted response vector
	y_pred = b[0] + b[1] * x
	# plotting the regression line
	plt.plot(x, y_pred, color = "g")
	# putting labels
	plt.xlabel('x')
	plt.ylabel('y')
	# function to show plot
	plt.show()

def test_with_numpy(data):
	xs = np.array([float(i[0]) for i in data])
	ys = np.array([float(i[1]) for i in data])
	b = estimate_coef(xs, ys)
	plot_regression_line(xs, ys, b)
	max_x = max(xs)
	min_x = min(xs)
	max_y = max(ys)
	min_y = min(ys)
	xs = np.array([(i - min_x) / (max_x - min_x) for i in xs])
	ys = np.array([(i - min_y) / (max_y - min_y) for i in ys])
	b = train_model(data, 0.0001)
	plot_regression_line(xs, ys, b)
	return

def read_data(file_name):
	fd = open(file_name, "r") #todo: remember to add close fd
	fd = [x.strip() for x in fd]
	print(fd)
	fd.pop(0)
	data = []
	for x in fd:
		values = x.split(",")
		data.append(values)
	print(data)
	return data

def main():
	if (len(sys.argv) == 2):
		file_name = sys.argv[1]
		data = read_data(file_name)
		test_with_numpy(data)
		# train_model(data)
	else:
		print("give the path to a csv file as argument")

main()
