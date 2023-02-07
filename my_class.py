import math
import os

#------------------------------------------------------------------------------
# Array class, recreate some functionalities of numpy arrays
# Array operations - + * and sum for multiplying, adding, substraction and pow
#------------------------------------------------------------------------------

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
# Linear Regression class
#------------------------------------------------------------------------

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
		return (loss)

#------------------------------------------------------------------------
# Try if a string can be converted to float
#------------------------------------------------------------------------

def is_float(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

#------------------------------------------------------------------------------------
# csv
# Reads a csv file and returns a list of lists that contain the values of each row.
# removes rows that are not convertible to float
#------------------------------------------------------------------------------------

# count commas in a string
def count_commas(length, string):
	comma = 0
	for a in range(length):
		if (string[a] == ","):
			comma += 1
	return comma

def validate_data(length, string):
	check_list = []
	# keep track of commas and dots
	for a in range(length):
		if (string[a] == ","):
			check_list.append(string[a])
		elif (string[a] == "."):
			check_list.append(string[a])
	check_list_len = len(check_list)
	# check that there are no more than one dot between commas
	for x in range(check_list_len):
		if (x > 0 and check_list[x] == "." and check_list[x - 1] == "."):
			return False
	check_list = []
	# keep track of - signs and dots
	for a in range(length):
		if (string[a] == ","):
			check_list.append(string[a])
		# if a - sign is not at the start of the number, it's not valid
		elif (string[a] == "-"):
			check_list.append(string[a])
			if (a > 0 and not string[a - 1] == ","):
				return False
	check_list_len = len(check_list)
	# check that there are no more than one "-" between commas
	for x in range(check_list_len):
		if (x > 0 and check_list[x] == "-" and check_list[x - 1] == "-"):
			return False
	return True

def validate_file(file_read):
	rows = len(file_read)
	comma_0 = 0
	comma_1 = 0
	# keep track of rows that need to be removed for having non valid characters
	to_remove = []
	for i in range(rows):
		row = len(file_read[i])
		comma_0 = count_commas(row, file_read[i])
		if (not validate_data(row, file_read[i])):
				print("Invalid .csv: too many dots or -")
				quit()
		for a in range(row):
			# comma, dot and - are valid characters, pass them
			if (file_read[i][a] == ","):
				pass
			elif (file_read[i][a] == "."):
				pass
			elif (file_read[i][a] == "-"):
				pass
			# keep track of the indexes of rows that have invalid characters
			elif (not is_float((file_read[i][a]))):
				to_remove.append(i)
				break
		if (i > 0):
			# check that each line is the same length as the first line
			if (not comma_0 - comma_1 == 0):
				print("Invalid .csv: uneven lines")
				quit()
		comma_1 = comma_0
		comma_0 = 0
	# update the index of the row to be removed
	to_remove_len = len(to_remove)
	for x in range(to_remove_len):
		to_remove[x] -= x
	# remove rows with invalid data
	for i in range(to_remove_len):
		file_read.pop(to_remove[i])
	return (file_read)

def read_csv_to_list(file_name):
	exists = os.path.isfile(file_name)
	if (exists):
		fd = open(file_name, "r")
		file_read = [x.strip() for x in fd]
		fd.close()
		i = 0
		file_read = validate_file(list(file_read))
		data = []
		for x in file_read:
			values = x.split(",")
			data.append(values)
		return data
	else:
		print("No file found.")
		quit()
