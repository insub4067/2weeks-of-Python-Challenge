import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from operator import itemgetter


"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""


def convert_to_int(x):
    if type(x) == float or type(x) == int:
        return x
    if "k" in x:
        if len(x) > 1:
            return float(x.replace("k", "")) * 1000
        return 1000.0
    return 0.0


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django",
]

db = {}


def get_soup(subreddit):
    res = requests.get(
        f"https://www.reddit.com/r/{subreddit}/top/?t=month", headers=headers
    ).text
    subreddit_soup = BeautifulSoup(res, "html.parser")
    divs = subreddit_soup.find("div", "rpBJOHq2PR60pnwJlUyP0")
    divs = divs.find_all("div", attrs={"data-testid": "post-container"})

    for div in divs:

        title = div.find("h3", "_eYtD2XCVieq6emjKBH3m").text
        votes = div.find("div", "_1E9mcoVn4MYnuBQSVDt1gC").text
        try:
            votes = int(votes)
        except:
            votes = int(convert_to_int(votes))
        url = div.find("a", href=True).get("href")
        catergory = subreddit
        promote = div.find("span", "_2oEYZXchPfHwcf9mTMGMg8")
        if promote is None:
            article = {
                "title": title,
                "votes": votes,
                "category": catergory,
                "url": url,
            }
            db[subreddit].append(article)


# app = Flask("DayEleven")
app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():

    return render_template("home.html", subreddits=subreddits)


@app.route("/read")
def read():

    articles = []

    selected = ""

    query = request.args
    for subreddit, value in query.items():
        db[subreddit] = []
        get_soup(subreddit)
        articles = articles + db[subreddit]
        selected = selected + f"r/{subreddit} "

    articles = sorted(articles, key=itemgetter("votes"), reverse=True)
    print(selected)

    return render_template("read.html", articles=articles, selected=selected)


# app.run(host="0.0.0.0")
if __name__ == "__main__":
    app.run(host="localhost", port="8003", debug=True)
