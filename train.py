import sys
import matplotlib.pyplot as plt
import my_class as my
# muista poistaa
import numpy as np

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
	learning_rate = 0.1
	regression = my.linear_regression(xs, ys)
	for i in range(iterations):
		y_preds = regression.predict(xs)
		# loss = regression.calculate_loss(y_preds)
		# losses.append(loss)
		regression.update_t(learning_rate)
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

# create a file "coefs.csv" and write the learned thetas there there
def save_coefs_to_file(coefs):
	fd = open("coefs.csv", "w")
	fd.close()
	fd = open("coefs.csv", "a")
	fd.write("t0,t1\n")
	fd.write(str(coefs[0])+","+str(coefs[1]))
	fd.close()

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
	save_coefs_to_file(b)
	plot_regression_line(xs, ys, b)
	return


def main():
	if (len(sys.argv) == 2):
		file_name = sys.argv[1]
		data = my.read_csv_to_list(file_name)
		test_with_numpy(data)
		# train_model(data)
	else:
		print("give the path to a csv file as argument")

main()
