import csv
from db import db


def export(word):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "comanpy", "location", "link"])
    jobs = db.get(word)
    for job in jobs:
        writer.writerow(job.values())
