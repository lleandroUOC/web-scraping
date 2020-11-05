# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:06:04 2020

@author: LuisL y EdnaE
"""


import requests
import pandas as panda
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
    
    listcourses = []
    url = "https://www.coursera.org/sitemap.xml"
    topic = "courses"
    listcourses = (processUrl(url, topic))    
    findClass(listcourses)

    
"""
Extract Dataset
""" 
def findClass(listcourses):
    
    CourseName = []
    CourseCategories = []
    CourseCategory = []
    CourseSubcategory = []
    Enrolled = []
    Difficulty = []
    Rating = []
    RatingCount = []
    print('inicio del proceso')
    
        for Course in listcourses:
        try: 
            webpage = requests.get(Course, timeout=15)
            soup = bs(webpage.content, 'html.parser')
            if((soup.find('h1', class_='banner-title m-b-0 banner-title-without--subtitle')) != None):
                CourseName.append( soup.find('h1', class_='banner-title m-b-0 banner-title-without--subtitle').get_text() )
            else: 
                CourseName.append('')
            CourseCategories = soup.find_all('a', class_='_172v19u6 color-white font-weight-bold')
            try:
                CourseCategory.append( CourseCategories[1].get_text() )
            except IndexError:
                CourseCategory.append('No Category')
            try:
                CourseSubcategory.append( CourseCategories[2].get_text() )
            except IndexError:
                CourseSubcategory.append('No Subcategory')
            if((soup.find('div',class_='rc-ProductMetrics')) != None):
                Enrolled.append( soup.find('div',class_='rc-ProductMetrics').find_all('span')[1].get_text() )
            else: 
                Enrolled.append('0')   
            if((soup.find('div', class_='_16ni8zai m-b-0 m-t-1s')) != None):            
                Difficultytemp = soup.find('div', class_='_16ni8zai m-b-0 m-t-1s').get_text()
                if(Difficultytemp == 'Advanced Level'):   
                    Difficulty.append('Advanced Level')
                elif(Difficultytemp == 'Intermediate Level'):
                    Difficulty.append('Intermediate Level')
                else:
                    Difficulty.append('Beginner Level')
            else: 
                Difficulty.append('0')
            if((soup.find('div', class_='rc-ReviewsOverview__totals__rating')) != None):
                Rating.append( soup.find('div', class_='rc-ReviewsOverview__totals__rating').get_text() )
            else: 
                Rating.append('')
            if((soup.find('div', class_='_wmgtrl9 color-white ratings-count-expertise-style')) != None):
                RatingCount.append( soup.find('div', class_='_wmgtrl9 color-white ratings-count-expertise-style').find('span').get_text() )
            else: 
                RatingCount.append('')
        except requests.exceptions.Timeout:
            print ('Timeout occurred')
        except requests.Timeout:
            print ('Timeout occurred')
        except requests.RequestException:
            print ('Timeout occurred')
    dataCourses = panda.DataFrame({'course_name': CourseName,
                          'course_category': CourseCategory,
                          'course_subcategory': CourseSubcategory,
                          'students_enrolled':Enrolled,
                          'course_difficulty':Difficulty,
                          'course_rating':Rating,
                          'course_rating_count':RatingCount})
    dataCourses.sort_values(by=['course_category'], inplace=True)
    dataCourses.to_csv('datacourses.csv')
    print('archivo generado')

        
        
processHtml()
