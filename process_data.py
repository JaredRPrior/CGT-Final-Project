from datetime import datetime, timedelta
# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py

def process_tuple_string(stocks):
	# processes stock tuple
	stock_d1 = stocks[0].replace("(", "")
	stock_d2 = stocks[1].replace(")", "")
	return float(stock_d1.strip()), float(stock_d2.strip())

def process_line(line):
	# processes each line in a 
	# text file formatted: publisher, article, date, stock prices @ date
	line = line.split(",")
	length = len(line)
	publisher = line[0]
	time = line[length - 3]
	stock_d1, stock_d2 = process_tuple_string(line[length - 2:])
	print(stock_d1, stock_d2)
	if stock_d2 != 0:
		return publisher, time, (stock_d1, stock_d2)
	else:
		return publisher, time, False

def process_file(file):
	# processes a file
	# calculates influence from publisher to stock
	for line in file.readlines():
		publisher, time, stocks = process_line(line)
		if stocks == False:
			continue
		else:
			delta = abs(stocks[1] - stocks[0])
			#print(delta)

def main():
	queries = ["AEG"]
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		process_file(f)
		f.close()

main()