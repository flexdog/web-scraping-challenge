# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 22:37:00 2020

@author: fbjba
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/MarsDB")


@app.route("/")
def home():
    #marsDataPull = mongo.db.scrape_data.find_one()
    marsDataPull = mongo.db.collection.find_one()
    return render_template("index.html", marsFacts=marsDataPull)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars2.scrape_info()
    #mongo.db.scrape_data.update({}, mars_data, upsert=True)
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
