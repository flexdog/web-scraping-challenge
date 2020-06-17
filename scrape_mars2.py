# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 00:28:55 2020

@author: fbjba
"""

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import re
from pymongo import MongoClient
import time
from datetime import datetime

def scrape_info():
     browser = Browser('chrome', headless=False)
     url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
     browser.visit(url)
     time.sleep(1)
     html = browser.html
     soup = bs(html, 'html.parser')
     latest_news = soup.find("li", class_="slide")
     news_title = latest_news.find("h3").text
     news_p = latest_news.find(class_="article_teaser_body").text
     
     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
     browser.visit(url)
     html = browser.html
     soup = bs(html, 'html.parser')
     base_url = "https://www.jpl.nasa.gov"
     style = soup.find(class_="main_feature").find(class_="carousel_items").article["style"]
     featured_image_url = base_url + style.split("url")[1].strip(";(')")
     
     url = 'https://twitter.com/marswxreport?lang=en'
     browser.visit(url)
     xpath = browser.find_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span')
     mars_weather = xpath.text
     
     url = 'https://space-facts.com/mars/'
     table = pd.read_html(url)
     space_facts_df = table[2]
     space_facts_df.rename(columns={0:'Description', 1:'Value'}, inplace=True)
     spaceFactsDF = space_facts_df.set_index('Description')
     mars_facts_dict = spaceFactsDF.to_dict()
     table_html = spaceFactsDF.to_html()
     
     browser.quit()
     
     hemisphere_image_urls = [
         {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov//cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
         {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov//cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
         {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov//cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
         {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov//cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
         ]
    
     
     datetime_now = datetime.now()
    
     mars_data = {
         "date": datetime_now,
         "news_title": news_title,
         "news_article": news_p,
         "featured_image_urll": featured_image_url,
         "mars_weather": mars_weather,
         "mars_facts": table_html,
         "urls": hemisphere_image_urls
         }
     
     return mars_data