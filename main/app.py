from flask import Flask, render_template, request, Response, redirect, url_for
from scraper import github_api, scrape_github
app = Flask(__name__)

result = ""

@app.route("/", methods=["POST", "GET"])
def home():
	global result
	search_term = ""
	if request.method == "POST":
		search_term = request.form["search"]
		if search_term != "":
			if request.form.get("action") == "scrape":
				result = scrape_github(search_term,1)
			elif request.form.get("action") == "api":
				result = github_api(search_term,1)
			return render_template("test.html", result=result, search_term=search_term)
		else:
			result = []
			return render_template("test.html", result=result, search_term=search_term)
	elif request.method == "GET":
		search_term = ""
		return render_template("test.html", result=result, search_term=search_term)

if __name__=='__main__':
	app.run(debug=True)