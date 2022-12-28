#!/usr/bin/python
import my_class as my

class theta:
	def __init__(self, t0, t1):
		self.t0 = t0
		self.t1 = t1

def estimate_price(mileage, coef):
	price = coef.t0 + coef.t1 * mileage
	return price

def read_coef():
	data = my.read_csv_to_list("coefs.csv")
	print(data)
	t0 = float(data[0][0])
	t1 = float(data[0][1])
	coef = theta(t0, t1)
	return coef

def main():
	mileage = float(input("Please input mileage to estimate price.\n"))
	coef = read_coef()
	estimated_price = estimate_price(mileage, coef)
	print("estimated price is: " + str(estimated_price))
main()
