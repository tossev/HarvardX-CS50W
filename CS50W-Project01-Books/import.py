import csv
from application import db

with open("books.csv") as f:
    reader = csv.reader(f)
    # Skip header
    next(reader)
    for isbn, title, author, pub_year in reader:
        db.execute("INSERT INTO books(isbn, title, author, pub_year) VALUES(:isbn, :title, :author, :pub_year)",
                   {"isbn": isbn, "title": title, "author": author, "pub_year": pub_year})
    db.commit()


