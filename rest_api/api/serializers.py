from flask_restplus import fields
from rest_api.api.restplus import api
import json


class Author(fields.Raw):
    def format(self, value):
        print(value)
        return json.dumps(value.__dict__)

book = api.model('Book', {
    'title': fields.String(required=True, description='Book title'),
    'isbn': fields.String(required=True, description='Book ISBN numer'),
    'pub_date': fields.Integer(required=True, description="Book pub date timestamp"),
    'authors': Author()
})

author = api.model('Author', {
    'name': fields.String(required=True, description='Author name'),
    'surname': fields.String(required=True, description='Author surname'),
})

author_with_books = api.inherit('Author books', author, {
    'books': fields.List(fields.Nested(book))
})

book_with_authors = api.inherit('Books authors', book, {
    'authors': fields.List(fields.Nested(author))
})
