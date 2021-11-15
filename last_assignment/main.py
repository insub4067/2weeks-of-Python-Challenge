from flask import Flask, render_template, request, send_file
from werkzeug.utils import redirect
from functions import get_jobs
from export import export
from db import keywords, db


app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():

    word = request.args.get("word")

    if word:
        word = word.lower()
        fromdB = db.get(word)
        if fromdB:
            jobs = fromdB
            amount = len(jobs)
            Word = word.capitalize()
            return render_template("result.html", jobs=jobs, word=Word, amount=amount)
        else:
            jobs = get_jobs(word)
            amount = len(jobs)
            db[word] = jobs
            Word = word.capitalize()
            return render_template("result.html", jobs=jobs, word=Word, amount=amount)

    return render_template("index.html", keywords=keywords)


@app.route("/search")
def search():
    word = request.args["word"].lower()
    jobs = get_jobs(word)
    amount = len(jobs)
    Word = word.capitalize()

    return render_template("result.html", jobs=jobs, word=Word, amount=amount)


@app.route("/export")
def file():

    word = request.args.get("word")
    if not word:
        raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
        raise Exception()
    export(word)
    return send_file("jobs.csv")


if __name__ == "__main__":
    app.run(host="localhost", port="8080", debug=True)
