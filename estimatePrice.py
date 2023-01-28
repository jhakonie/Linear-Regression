#!/usr/bin/python
import os
import my_class as my

#--------------------------------------------------------------------------------------------------
class theta:
	def __init__(self, t0, t1):
		self.t0 = t0
		self.t1 = t1
#--------------------------------------------------------------------------------------------------

def estimate_price(mileage, coef):
	price = coef.t0 + coef.t1 * mileage
	return price
	
#--------------------------------------------------------------------------------------------------

def read_coef(file_name):
	# if there is a file with the thetas saved, read it
	exists = os.path.exists(file_name)
	if (exists):
		data = my.read_csv_to_list(file_name)
		t0 = float(data[0][0])
		t1 = float(data[0][1])
		coef = theta(t0, t1)
		return coef
	# if there isn't, train a model and ask for a file name or quit
	else:
		user_input = input("No model trained, train model? y/n\n")
		if (user_input == "y"):
			user_file_name = input("Please insert .csv file name to train model with.\n")
			command = "python3 train.py "+user_file_name
			os.system(command)
			coef = read_coef("coefs.csv")
			return (coef)
		else:
			user_input = input("Do you already have thetas saved in a .csv file? y/n\n")
			if (user_input == "y"):
				user_file_name = input("Please insert .csv file name to use as thetas.\n")
				coef = read_coef(user_file_name)
				return (coef)
			else:
				print("Unable to predict price, quit.")
				quit()
				
#--------------------------------------------------------------------------------------------------

def main():
	mileage = input("Please input mileage to estimate price.\n")
	while (1):
		if (my.is_float(mileage)):
			mileage = float(mileage)
			if (mileage < 0):
				mileage = "NA"
				continue
			break
		else:
			mileage = input("Please input proper mileage to estimate price.\n")
	coef = read_coef("coefs.csv")
	estimated_price = estimate_price(mileage, coef)
	if (estimated_price < 0):
		estimated_price = 0
	print("estimated price is: " + str(estimated_price))
main()
