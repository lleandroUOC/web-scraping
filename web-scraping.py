# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:06:04 2020

@author: LuisL
"""


import requests
from bs4 import BeautifulSoup as bs




"""
Function to get sitemap url from main site map according to topic name
For example get the url related to courses
"""
def getSiteMapUrl(url, topic):

    result = ""

    response = requests.get(url)

    soup = bs(response.text, features="lxml")

    elements = soup.find_all("loc")

    
    for element in elements:

        if element.text.find(topic) > 0:
            result = element.text

    
    return result
    
"""
Get all links from url
"""    
def getLinks(url):
    
    links = []
    
    response = requests.get(url)

    soup = bs(response.text, features="lxml")

    elements = soup.find_all("loc")
    
    for element in elements:
        links.append(element.text)
    
    return links

"""

"""
def processUrl(url, topic):
    
    siteMapUrl = getSiteMapUrl(url, topic)
    return getLinks(siteMapUrl)


"""
Process url with specific topic
"""
def processHtml():
    
    url = "https://www.coursera.org/sitemap.xml"
    topic = "courses"
    print(processUrl(url, topic))
    

processHtml()
