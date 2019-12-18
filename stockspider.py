import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import json
import urllib
import htmldate
import requests

def url_gen(query, page_number):
    # generates a URL for a Google News query
    url = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=nws&start=" + str(page_number - 1) + "0"
    return url

def get_data(url, browser, page_number, ceiling, data):
    # retrives data from given URL, recursively crawls entire news query
    # until the crawler has reached the page ceiling, or there are no
    # more pages left to crawl in the results

    browser.get(url)
    browser.implicitly_wait(30)
    table = browser.find_element_by_css_selector("tbody")
    max_page = table.find_elements_by_css_selector("a")
    elem = browser.find_elements_by_css_selector("div.bkWMgd")
    for i in elem:
        author = i.find_elements_by_css_selector("a")
        for a in author:
            publisher = i.find_element_by_css_selector("div.pDavDe.RGRr8e")
            title = i.find_element_by_css_selector("div.phYMDf.nDgy9d")  
            try:
                r = requests.get(a.get_attribute('href'), verify=False)
                date_published = htmldate.find_date(r.text)
                data.append(publisher.text, title.text, date_published)
            except:
                print(publisher.text, title.text)
    if max_page != None and page_number < ceiling:
        get_data(max_page[len(max_page) - 1].get_attribute('href'), browser, page_number + 1, ceiling)

def main():
    browser = webdriver.Safari()
    ceiling = 15
    queries = ["rekr+stock"]
    data = []
    for query in queries:
        url = url_gen(query, 1)
        get_data(url, browser, 0, ceiling, data)



main()