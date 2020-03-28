from flask_restplus import fields
from rest_api.api.restplus import api

book = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='Book id'),
    'title': fields.String(required=True, description='Book title'),
    'isbn': fields.String(required=True, description='Book ISBN numer'),
    'pub_date': fields.DateTime,
    'author': fields.String(attribute='author.id'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_author_books = api.inherit('Page of author books', pagination, {
    'items': fields.List(fields.Nested(book))
})

author = api.model('Author', {
    'name': fields.String(required=True, description='Author name'),
    'surname': fields.String(required=True, description='Author surname'),
})

author_with_books = api.inherit('Author books', author, {
    'books': fields.List(fields.Nested(book))
})
