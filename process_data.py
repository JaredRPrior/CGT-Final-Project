from datetime import datetime, timedelta
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py

def write_results(file, results, ranking_by):
	# writes output rankings to result file
	rank = 1
	file.write(ranking_by)
	file.write("\n")
	for i in results:
		file.write(str(rank) + ": ")
		file.write(str(i))
		file.write("\n")
		rank += 1
	file.write("\n")

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

def represent_undirected_graph(graph):
	# takes all edges from stock -> publisher, creates {{}...} such that publisher -> stock
	aux_graph = {}
	for i in graph:
		for publisher in graph[i]:
			try:
				aux_graph[publisher][i] = graph[i][publisher]
			except:
				aux_graph[publisher] = {}
				aux_graph[publisher][i] = graph[i][publisher]

	return aux_graph

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
			delta_absolute = abs(stocks[1] - stocks[0])/stocks[0]
			delta = (stocks[1] - stocks[0])/stocks[0]
			try: 
				publisher_influence[publisher].append((delta_absolute, delta))
			except:
				publisher_influence[publisher] = []
			publisher_influence[publisher].append((delta_absolute, delta))

	return publisher_influence

def process_dictionary_helper(absolute, positive, negative, dictionary, publisher):
	# takes each change tuple and assembles absolute, positive, negative change lists
	# creates a three-tuple as the value for each publishers
	change = dictionary[publisher]
	size = len(change)
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

	dictionary[publisher] = (absolute, positive, negative, size)
	return dictionary

def process_dictionary(dictionary):
	# aggregate the percent change values
	for publisher in dictionary:
		positive = []
		negative = []
		absolute = []
		dictionary = process_dictionary_helper(absolute, positive, negative, dictionary, publisher)
	return dictionary

def plot_ranking(results, sort_index, label):
	# credit to https://pythonspot.com/matplotlib-bar-chart/
	objects = []
	performance = []
	plt.figure(figsize= (20, 15))
	i = 0
	while i < 10:
		objects.append(results[i][0])
		performance.append(results[i][sort_index])
		i += 1
	x_pos = np.arange(len(objects))
	plt.barh(x_pos, performance, align='center', alpha=0.8)
	plt.yticks(x_pos, objects, fontsize=10)
	#plt.xlabel('Percent change')
	plt.title(label)
	plt.savefig(str(sort_index) +".png")
	plt.close()

def sort_results(results, sort_index):
	# sort and reverse a list by a certain index of the result tuple
	results.sort(key=lambda x: x[sort_index])
	results.reverse()
	return results

def main():
	queries = ["AEG", "POLA", "CSLT", "REFR", "SEAC", "SMSI", "REKR", "ENSV", "OCLN", "SING", "USMJ"]
	graph = {}
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		data = process_file(f)
		processed_data = process_dictionary(data)
		graph[file] = processed_data
		f.close()
	aux_graph = represent_undirected_graph(graph)
	results = []
	for publisher in aux_graph:
		positive = []
		negative = []
		absolute = []
		size = 0
		for stock in aux_graph[publisher]:
			absolute += aux_graph[publisher][stock][0]
			positive += aux_graph[publisher][stock][1]
			negative += aux_graph[publisher][stock][2]
			size += aux_graph[publisher][stock][3]
		negative = mean_average(negative)
		positive = mean_average(positive)
		results.append((publisher, mean_average(absolute) * 100, positive * 100, negative * 100, len(aux_graph[publisher]), size, (positive + negative) * 100))

	f = open("results.txt", "w")

	results = sort_results(results, 1)
	plot_ranking(results, 1, "Mean Absolute Influence")
	write_results(f, reversed(results), "Mean absolute influence")

	results = sort_results(results, 2)
	plot_ranking(results, 2, "Mean Positive Influence")
	write_results(f, reversed(results), "Mean positive influence")

	results = sort_results(results, 3)
	results.reverse()
	plot_ranking(results, 3, "Mean Negative Influence")
	write_results(f, results, "Mean negative influence")

	results = sort_results(results, 4)
	plot_ranking(results, 4, "Publisher degree")
	write_results(f, results, "Publisher degree")

	results = sort_results(results, 5)
	plot_ranking(results, 5, "Articles Published")
	write_results(f, results, "Articles published")

	results = sort_results(results, 6)
	plot_ranking(results, 6, "Sum of Mean Negative and Positive Influence")
	write_results(f, reversed(results), "Sum of mean negative and positive influence")

	f.close()



main()