from datetime import datetime, timedelta
# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py



def average_delta(dictionary):
	# average out the percent change values
	for publisher in dictionary:
		value_sum = 0
		for value in dictionary[publisher]:
			value_sum += value
		average = value_sum/len(dictionary[publisher])
		dictionary[publisher] = average
	return dictionary

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
	if stock_d2 == 0:
		return False
	else:
		return publisher, time, (stock_d1, stock_d2)

def process_file(file):
	# processes a file
	# calculates influence from publisher to stock
	publisher_influence = {}
	for line in file.readlines():
		if process_line(line) == False:
			continue
		else:
			publisher, time, stocks = process_line(line)
			delta = abs(stocks[1] - stocks[0])
			try: 
				publisher_influence[publisher].append(delta)
			except:
				publisher_influence[publisher] = []
			publisher_influence[publisher].append(delta)

	return publisher_influence

def main():
	queries = ["AEG"]
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		data = process_file(f)
		processed_data = average_delta(data)
		for i in processed_data:
			print(i, processed_data[i])
		f.close()

main()