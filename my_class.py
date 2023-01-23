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

	def sum_pow(self, num):
		result = 0
		for i in range(self.size):
			temp_result = 1
			for a in range(num):
				temp_result *= self.array[i]
			result += temp_result
			# result += self.array[i] * self.array[i]
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
		loss = (y_preds - self.ys).sum_pow(2) / n
		# print(loss)
		return loss

#------------------------------------------------------------------------
# try if string is float

def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

#------------------------------------------------------------------------
# csv
# Reads a csv file and returns a list, where each item a list of items on a row.
# removes the first row if it's not convertible to float

def validate_file(file_read):
	# i = 0
	rows = len(file_read)
	comma_0 = 0
	comma_1 = 0
	# print(len(file_read[1]))
	# print(file_read[1][1])
	for i in range(rows - 1):
		# print(file_read)
		# print(len(file_read))
		row = len(file_read[i])
		for a in range(row - 1):
			if (file_read[i][a] == ","):
				comma_0 += 1
			elif (not is_float((file_read[i][a]))):
				file_read.pop(i)
				# return (False)
		if (i > 0):
			if (not comma_0 - comma_1 == 0):
				return (False)
		comma_1 = comma_0
		comma_0 = 0
	# for x in file_read:
	# 	if (not is_float(x)):
	# 		file_read.pop(i)
	# 		i += 1
	return True

def read_csv_to_list(file_name):
	exists = os.path.exists(file_name)
	if (exists):
		fd = open(file_name, "r")
		file_read = [x.strip() for x in fd]
		fd.close()
		i = 0
		if (not validate_file(file_read)):
			print("Invalid .csv")
			quit()
		data = []
		for x in file_read:
			values = x.split(",")
			data.append(values)
		print (data)
		return data
	else:
		print("No file found.")
		quit()
