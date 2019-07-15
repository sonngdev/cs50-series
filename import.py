import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    authors = {}
    counter = 1

    next(reader)

    for isbn, title, author, year in reader:
        if not authors.get(author):
            db.execute("INSERT INTO authors (id, name) VALUES (:id, :name)",
                        {"id": counter, "name": author})
            print(f"Added author with id: {counter}, name: {author}.")
            authors[author] = counter
            counter += 1

        author_id = authors.get(author)
        db.execute("INSERT INTO books (isbn, title, year, author_id) VALUES (:isbn, :title, :year, :author_id)",
                    {"isbn": isbn, "title": title, "year": year, "author_id": author_id})
        print(f"Added book with isbn: {isbn}, title: {title}, year: {year}, author_id: {author_id}.")

    db.commit()

if __name__ == "__main__":
    main()
