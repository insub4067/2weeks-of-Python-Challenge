import requests
from flask import Flask, render_template, request


base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
# app = Flask("DayNine")
app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():

    pop_posts = requests.get(popular).json()["hits"]
    db["popular"] = pop_posts

    new_posts = requests.get(new).json()["hits"]
    db["new"] = new_posts

    order = request.args.get("order_by")

    if order:
        if order == "new":
            return render_template("index.html", posts=db["new"], orderBy=order)
        if order == "popular":
            return render_template("index.html", posts=db["popular"], orderBy=order)
    else:
        return render_template("index.html", posts=db["popular"], orderBy="popular")


@app.route("/<id>")
def comments(id):
    url = f"{base_url}/items/{id}"
    comments = requests.get(url).json()
    return render_template("detail.html", comments=comments)


# app.run(host="0.0.0.0")
if __name__ == "__main__":
    app.run(host="localhost", port="8001", debug=True)
