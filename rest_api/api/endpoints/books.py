import logging

from flask import request
from flask_restplus import Resource
import time
from datetime import datetime, date

from rest_api.api.serializers import book, book_with_authors
from rest_api.api.restplus import api
from rest_api.database.models import Book, Author, db

log = logging.getLogger(__name__)

ns = api.namespace('books', description='Operations related to books')


@ns.route('/')
class BooksCollection(Resource):

    @api.marshal_list_with(book)
    def get(self):
        """
        Returns list of books.
        """
        books = Book.query.all()
        return books

    @api.expect(book)
    def post(self):
        """
        Creates a new book.
        """
        data = request.json

        book_id = data.get('id')
        title = data.get('title')
        isbn = data.get('isbn')
        pub_date = date.fromtimestamp(data.get("pub_date_timestamp"))

        author_id = data.get('author_id')
        author_obj = Author.query.filter(Author.id == author_id).one()

        book_obj = Book(title, isbn, [author_obj], pub_date)
        book_obj.authors.append(author_obj)
        if book_id:
            book_obj.id = author_id

        db.session.add(book_obj)
        db.session.commit()
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Book not found.')
class PostItem(Resource):

    @api.marshal_with(book_with_authors)
    def get(self, id):
        """
        Returns a book with authors.
        """
        return Book.query.filter(Book.id == id).one()

    @api.expect(book)
    @api.response(204, 'Book successfully updated.')
    def put(self, id):
        """
        Updates a book.
        """
        data = request.json
        book_obj = Book.query.filter(Book.id == id).one()
        book_obj.title = data.get('title')
        book_obj.isbn = data.get('isbn')
        book_obj.pub_date = date.fromtimestamp(data.get("pub_date_timestamp"))

        author_id = data.get('author_id')
        author_obj = Author.query.filter(Author.id == author_id).one()
        book_obj.authors.append(author_obj)

        db.session.add(book_obj)
        db.session.commit()
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes book.
        """
        book = Book.query.filter(Book.id == id).one()
        db.session.delete(book)
        db.session.commit()
        return None, 204
