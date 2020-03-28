# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import date

from rest_api.database import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    isbn = db.Column(db.String(80))
    pub_date = db.Column(db.Date)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    authors = db.relationship('Author', backref=db.backref('books', lazy='dynamic'))

    def __init__(self, title, isbn, authors, pub_date=None):
        self.title = title
        self.isbn = isbn
        if pub_date is None:
            pub_date = date.today()
        self.pub_date = pub_date
        self.authors = authors

    def __repr__(self):
        authors = ", ".join(self.authors)
        return f'<Book {self.title} {authors} {self.isbn} pub_date: {self.pub_date}>'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'<Author {self.name} {self.surname}>'
