#!/usr/bin/python
import os
import my_class as my

class theta:
	def __init__(self, t0, t1):
		self.t0 = t0
		self.t1 = t1

def estimate_price(mileage, coef):
	price = coef.t0 + coef.t1 * mileage
	return price

def read_coef():
	exists = os.path.exists("coefs.csv")
	if (exists):
		data = my.read_csv_to_list("coefs.csv")
		t0 = float(data[0][0])
		t1 = float(data[0][1])
		coef = theta(t0, t1)
		return coef
	else:
		user_input = input("No model trained, train model now with data.csv? y/n\n")
		if (user_input == "y"):
			os.system("python3 train.py 1data.csv")
			coef = read_coef()
			return (coef)
		else:
			print("Unable to predict price without a model, quit.")
			quit()

def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def main():
	mileage = input("Please input mileage to estimate price.\n")
	while (1):
		if (is_float(mileage)):
			mileage = float(mileage)
			if (mileage < 0):
				mileage = "NA"
				continue
			break
		else:
			mileage = input("Please input proper mileage to estimate price.\n")
	coef = read_coef()
	estimated_price = estimate_price(mileage, coef)
	if estimated_price < 0:
		estimated_price = 0
	print("estimated price is: " + str(estimated_price))
main()
