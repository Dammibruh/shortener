'''
MIT License

Copyright (c) 2020 dammi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from flask import (
    Flask, redirect, request, url_for, jsonify, Response, render_template
    )
import time
import re
import string
import psycopg2
import os
from datetime import datetime
import random


app = Flask(__name__)

uri = os.environ["DATABASE_URL"]
conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS shortlmao (url TEXT, shortened TEXT, requester TEXT, date TEXT)")

@app.route("/home/")
@app.route("/")
def main():
	return "post /shortener"


@app.route("/shortener/", methods=["POST", "GET"])
def shortener():
	if request.method == "POST":
		url = request.form.get("url")
		if re.match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",url):
			date = str(datetime.utcnow())
			shortened = request.form.get("shortenerd")
			cur.execute("INSERT INTO shortlmao (url, shortened, requester, date) VALUES(%s, %s, %s, %s)",(url, shortened, "null", date))
			conn.commit()
			return jsonify({"url":url, "shortened":shortened})
		else:
			return jsonify({"error":"Invalid url provided"}), 406
	return jsonify({"url":None, "shortened": None})

@app.route("/shortener/<string:name>/")
def urlredi(name):
	data = cur.execute("SELECT * FROM shortlmao WHERE shortened = %s",(name,))
	check = cur.fetchall()
	print(check)
	return jsonify({"org_url":check})
@app.errorhandler(KeyError)
def shortnotfound(e):
		return jsonify({"error": 404}), 404
conn.commit()
