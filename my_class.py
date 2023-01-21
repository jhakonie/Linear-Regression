import math
import os

#------------------------------------------------------------------------------
# Array operations - + * and sum for multiplying, adding, substraction and pow

class arr:
	def __init__(self, array):
		self.array = array
		self.size = len(self.array)

	def __add__(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = []
		if (n != self.size):
			print("arrays must be same size to add them")
			m = max(n, self.size)
			for i in range(m):
				result.append(0)
			return result
		for i in range(n):
			result.append(self.array[i] + other.array[i])
		return (arr(result))

	def __sub__(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = []
		if (n != self.size):
			print("arrays must be same size to substract them")
			m = max(n, self.size)
			for i in range(m):
				result.append(0)
			return result
		for i in range(n):
			result.append(self.array[i] - other.array[i])
		return (arr(result))

	def __mul__(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = []
		if (n != self.size):
			print("arrays must be same size to multiply them")
			m = max(n, self.size)
			for i in range(m):
				result.append(0)
			return result
		for i in range(n):
			result.append(self.array[i] * other.array[i])
		return (arr(result))

	def sum_add(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = 0
		if (n != self.size):
			print("arrays must be same size to add them")
			return -1
		for i in range(n):
			result += self.array[i] + other.array[i]
		return result

	def sum_self(self):
		n = self.size
		result = 0
		for i in range(n):
			result += self.array[i]
		return result

	def sum_substract(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = 0
		if (n != self.size):
			print("arrays must be same size to substract them")
			return -1
		for i in range(n):
			result += self.array[i] - other.array[i]
		return result

	def sum_multiply(self, other):
		other = other if isinstance(other, arr) else arr(other)
		n = other.size
		result = 0
		if (n != self.size):
			print("arrays must be same size to multiply them")
			return -1
		for i in range(n):
			result += self.array[i] * other.array[i]
		return result

	def sum_pow(self):
		result = 0
		for i in range(self.size):
			result += self.array[i] * self.array[i]
		return result

	def multiply_scalar(self, scalar):
		result = []
		for i in range(self.size):
			result.append(self.array[i] * scalar)
		return result

#------------------------------------------------------------------------
# Linear Regression

class linear_regression:
	def __init__(self, xs, ys):
		# using my own arr-class to make sums easier to write, numpy is forbidden in this project
		self.xs = arr(xs)
		self.ys = arr(ys)
		self.t = [0, 0]
		# self.gradient = [0, 0]

	def update_t(self, learning_rate):
		y_preds = self.predict()
		ys = self.ys
		xs = self.xs
		n = float(ys.size)

		# sum of predicted y-values - true y-values
		y_difference = y_preds - ys
		self.t[0] = self.t[0] - (learning_rate * (1 / n) * y_difference.sum_self())
		self.t[1] = self.t[1] - (learning_rate * (1 / n) * (y_difference * xs).sum_self())

	def predict(self, xs = []): #estimate_mileage
		y_preds = []
		if not xs: xs = self.xs
		xs = xs if isinstance(xs, arr) else arr(xs)
		t = self.t
		n = xs.size
		for i in range(n):
			y_preds.append((xs.array[i] * t[1] + t[0]))
		return (arr(y_preds))

	def calculate_loss(self, y_preds):
		y_preds = y_preds if isinstance(y_preds, arr) else arr(y_preds)
		n = self.ys.size
		loss = (1 / (2 * n)) * (y_preds - self.ys).sum_pow()
		return loss



#------------------------------------------------------------------------
# csv
# Reads a csv file and returns a list, where each item a list of items on a row.
# removes the first row if it's not convertible to float

def read_csv_to_list(file_name):
	exists = os.path.exists(file_name)
	if (exists):
		fd = open(file_name, "r") #todo: remember to add close fd
		file_read = [x.strip() for x in fd]
		fd.close()
		file_read.pop(0)
		data = []
		for x in file_read:
			values = x.split(",")
			data.append(values)
		return data
	else:
		print("No file found.")
		quit()
