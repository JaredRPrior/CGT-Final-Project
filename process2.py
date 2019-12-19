from datetime import datetime, timedelta
# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py

def represent_undirected_graph(graph):
	# might not need it 
	# takes all edges from stock -> publisher, creates publisher -> stock
	aux_graph = {}
	for i in graph:
		for publisher in graph[i]:
			try:
				aux_graph[publisher][i] = graph[i][publisher]
			except:
				aux_graph[publisher] = {}
				aux_graph[publisher][i] = graph[i][publisher]

	return aux_graph

def mean_average(array):
	# find the mean average of an int/float array
	if len(array) == 0:
		return 0
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

def process_helper(absolute, positive, negative, dictionary, publisher):
	change = dictionary[publisher]
	for i in change:
		absolute.append(i[0])
		if i[1] > 0:
			positive.append(i[1])
		elif i[1] < 0:
			negative.append(i[1])
	if len(positive) == 0:
			positive = []
	if len(negative) == 0:
			negative = []
		# average = absolute_sum/len(dictionary[publisher])

	dictionary[publisher] = (absolute, positive, negative)
	return dictionary

def process_dictionary(dictionary):
	# aggregate the percent change values
	for publisher in dictionary:
		positive = []
		negative = []
		absolute = []
		dictionary = process_helper(absolute, positive, negative, dictionary, publisher)
	return dictionary

def main():
	queries = ["AEG", "POLA", "CSLT", "REFR", "SEAC", "SMSI", "REKR", "ENSV"]
	graph = {}
	result_dictionary = {}
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		data = process_file(f)
		processed_data = process_dictionary(data)
		graph[file] = processed_data
		f.close()
	aux_graph = represent_undirected_graph(graph)
	for publisher in aux_graph:
		positive = []
		negative = []
		absolute = []
		for stock in aux_graph[publisher]:
			positive += aux_graph[publisher][stock][1]
			negative += aux_graph[publisher][stock][2]
			absolute += aux_graph[publisher][stock][0]

		print(publisher, mean_average(positive), mean_average(negative), mean_average(absolute), len(aux_graph[publisher]))
		print(" ")
			

	#print(aux_graph)

main()