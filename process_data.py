from datetime import datetime, timedelta
# Jared Prior, Ian Culnane
# processes data scraped by stockspider.py

def process_line(line):
	# processes each line in a 
	# text file formatted: publisher, article, date, stock prices @ date
	line = line.split(",")
	publisher = line[0]
	time = line[2]
	stocks = line[3]
	if stocks[1] != 0:
		return publisher, time, stocks
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
			print(delta)

def main():
	queries = ["AEG", "POLA", "CSLT", "REFR", "SEAC", "SMSI", "REKR", "ENSV"]
	for file in queries:
		file_name = file + ".txt"
		f = open(file_name, "r")
		process_file(f)
		f.close()

main()