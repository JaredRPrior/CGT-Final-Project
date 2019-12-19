from datetime import datetime, timedelta
# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py

def represent_undirected_graph(graph):
	# might not need it 
	# takes all edges from stock -> publisher, creates publisher -> stock
	for i in graph:
		for publisher in graph[i]:
			print(i, publisher)
			try:
				graph[publisher][i] = graph[i][publisher]
			except:
				graph[publisher] = {}
				graph[publisher][i] = graph[i][publisher]
	return graph

def mean_average(array):
	# find the mean average of an int/float array
	average = 0
	for i in array:
		average += i
	average = average/len(array)
	return average

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
	if stock_d2 == 0 or abs(stock_d1 - stock_d2) == 0:
		return False
	else:
		return publisher, time, (stock_d1, stock_d2)

def process_file(file):
	# processes a file
	# gathers data about publisher influence over given stock
	publisher_influence = {}
	for line in file.readlines():
		if process_line(line) == False:
			continue
		else:
			publisher, time, stocks = process_line(line)
			delta_absolute = abs(stocks[1] - stocks[0])
			delta = stocks[1] - stocks[0]
			try: 
				publisher_influence[publisher].append((delta_absolute, delta))
			except:
				publisher_influence[publisher] = []
			publisher_influence[publisher].append((delta_absolute, delta))

	return publisher_influence

def process_helper(absolute_sum, positive, negative, dictionary, publisher):
	for change in dictionary[publisher]:
			absolute_sum += change[0]
			if change[1] > 0:
				positive.append(change[1])
			elif change[1] < 0:
				negative.append(change[1])
	if len(positive) == 0:
		positive = 0
	else:
		positive = mean_average(positive)
	if len(negative) == 0:
		negative = 0
	else:
		negative = mean_average(negative)
	average = absolute_sum/len(dictionary[publisher])
	dictionary[publisher] = (average, positive, negative)
	return dictionary

def process_dictionary(dictionary):
	# average out the percent change values
	for publisher in dictionary:
		positive = []
		negative = []
		absolute_sum = 0
		dictionary = process_helper(absolute_sum, positive, negative, dictionary, publisher)
	return dictionary

def main():
	queries = ["AEG", "POLA", "CSLT", "REFR", "SEAC", "SMSI", "REKR", "ENSV"]
	graph = {}
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		data = process_file(f)
		processed_data = process_dictionary(data)
		graph[file] = processed_data
		f.close()
		#graph = represent_undirected_graph(graph)
		print(file, graph[file], len(graph[file]))
		print(" ")

main()