from flask import Flask, render_template, request, Response, redirect, url_for
from scraper import github_api, scrape_github
app = Flask(__name__)

result = ""

@app.route("/", methods=["POST", "GET"])
def home():
	global result
	if request.method == "POST":
		search_term = ""
		search_term = request.form["search"]
		if search_term is not "":
			if request.form.get("action") == "scrape":
				result = scrape_github(search_term,1)
			elif request.form.get("action") == "api":
				result = github_api(search_term,1)
			return render_template("test.html", result=result)
		else:
			result = ["Could not find anything"]
			return render_template("test.html", result=result)
	elif request.method == "GET":
		return render_template("test.html", result=result)

if __name__=='__main__':
	app.run(debug=True)