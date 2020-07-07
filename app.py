from flask import Flask, redirect, request, url_for, jsonify, Response, render_template
import time
import re
import string
import psycopg2
import os
from datetime import datetime
import random


app = Flask(__name__)

page = {"name" : "MIURL"}
uri = os.environ["DATABASE_URL"]
conn = psycopg2.connect(uri)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS shortlmao (url TEXT, shortened TEXT, requester TEXT, date TEXT)")

@app.route("/home/")
@app.route("/")
def main():
	return render_template("home.html", page=page)


@app.route("/shortener/", methods=["POST", "GET"])
def shortener():
	if request.method == "POST":
		url = request.form.get("url")
		if re.match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",url):
			requester_ip = str(request.remote_addr)
			name = "".join(random.choices(string.hexdigits, k=12))
			date = str(datetime.utcnow())
			shortened = f"{request.url_root}shortener/{name}/"
			cur.execute("INSERT INTO shortlmao (url, shortened, requester, date) VALUES(%s, %s, %s, %s)",(url, shortened, requester_ip, date))
			conn.commit()
			return render_template("index.html", page=page, urlsh=shortened)
		else:
			return render_template("index.html", page=page, urlsh="Invalid url provided"), 406
	return render_template("index.html", page=page)

@app.route("/shortener/<string:name>/")
def urlredi(name):
	data = cur.execute("SELECT * FROM shortlmao WHERE shortened = %s",(f"{request.url_root}shortener/{name}/",))
	check = cur.fetchall()
	print(check[0][0])
	return redirect(check[0][0])
	
@app.errorhandler(404)
def pagenotfound(e):
	return render_template("404.html",name="Page not found", error=f"Looks like the page you requested wasn't found"), 404
	
@app.errorhandler(KeyError)
def shortnotfound(e):
		return render_template("404.html",name="URL not found", error=f"Looks like the shortened url you requested wasn't found"), 404
		
@app.route("/contact/", methods=["GET", "POST"])
def contact():
	email = ""
	name = ""
	content = ""
	return "", 401
conn.commit()
