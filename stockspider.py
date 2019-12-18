from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
import os
import json
import urllib
import htmldate
import requests
import yfinance as yf
from datetime import datetime, timedelta

def url_gen(query, page_number):
    # generates a URL for a Google News query
    url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=nws&start=" + str(page_number - 1) + "0"
    return url

def increment_date(date):
    # taken and adapted from https://stackoverflow.com/questions/37089765/add-1-day-to-my-date-in-python
    date2 = datetime.strptime(date, "%Y-%m-%d")
    date2 = date2 + timedelta(days=1)
    datetime.strftime(date2, "%Y-%m-%d")
    date2= str(date2).split(" ")[0]
    return date2

def retrieve_stock_info(stock, date):
    # uses yfinance to retrieve stock data for the given dates
    date2 = increment_date(date)
    data = yf.download(stock, date, date2)
    if len(data['Close']) > 1:
        return (data['Close'][0], data['Close'][1])
    else:
        return (data['Close'][0], 0)

def write_file(a, outfile, publisher, stock, title):
    # writes data to a file
    r = requests.get(a.get_attribute('href'), verify=False)
    date_published = htmldate.find_date(r.text)
    stock_info = retrieve_stock_info(stock, date_published)
    file = open(outfile,"a")
    string = publisher.text + ", " + title.text.replace("\n", "") + ", " + date_published + ", " + str(stock_info)
    file.write(string)
    file.write("\n")
    file.close()

def get_data(url, browser, page_number, ceiling, outfile, stock):
    # retrives data from given URL, recursively crawls entire news query
    # until the crawler has reached the page ceiling, or there are no
    # more pages left to crawl in the results
    print(page_number)
    browser.get(url)
    browser.implicitly_wait(30)
    table = browser.find_element_by_css_selector("tbody")
    next_page = table.find_elements_by_css_selector("a")
    elem = browser.find_elements_by_css_selector("div.bkWMgd")

    for i in elem:
        author = i.find_elements_by_css_selector("a")
        for a in author:
            publisher = i.find_element_by_css_selector("div.pDavDe.RGRr8e")
            title = i.find_element_by_css_selector("div.phYMDf.nDgy9d")  
            try:
                write_file(a, outfile, publisher, stock, title)
            except:
                print("Exception")
    if next_page != None and page_number < ceiling:
        url = next_page[len(next_page) - 1].get_attribute('href')
        get_data(url, browser, page_number + 1, ceiling, outfile, stock)

def main():
    browser = webdriver.Safari()
    ceiling = 15
    queries = ["AEG", "POLA", "CSLT", "REFR", "SEAC", "SMSI", "REKR", "ENSV"]
    for query in queries:
        url = url_gen(query + "+stock", 1)
        outfile = query + ".txt"
        get_data(url, browser, 0, ceiling, outfile, query)
        print("One query scraped.")

main()