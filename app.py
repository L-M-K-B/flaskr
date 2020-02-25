from flask import Flask, jsonify, request, abort
from models import setup_db, Book
from flask_cors import CORS

##--## helpers ##--##

books_per_shelf = 4


def paginate_books(selection):
    page = request.args.get('page', 1, type=int)

    start = (page - 1) * books_per_shelf
    end = start + books_per_shelf

    formatted_books = [book.format() for book in selection]
    current_books = formatted_books[start:end]

    return current_books

##--## -------- ##--##


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # CORS(app, resources={r"*/api/*": {origins: '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS  ')
        return response

    #--# removed in FlaskII lesson #--#
    # @app.route('/')
    # # @cross_origin
    # def hello():
    #     return jsonify({'message': 'Hello?'})

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        pagination = paginate_books(books)
        # zweite Seite aufrufbar mit: http://127.0.0.1:5000/books?page=2

        if len(pagination) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': pagination,
            'total_books': len(books)
        })

    @app.route('/books/<int:book_id>')
    def get_specific_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()

        if book is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'book': book.format()
            })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            # nur rating kann geupdated werden
            if 'rating' in body:
                book.rating = int(body.get('rating'))

            book.update()

            return jsonify({
                'success': True,
                'id': book.id
            })

        except:
            abort(404)
        # for testing PATCH: curl http://127.0.0.1:5000/books/10 -X PATCH -H "Content-Type: application/json" -d '{"rating":"9"}'

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            book.delete()
            books = Book.query.all()
            pagination = paginate_books(books)

            return jsonify({
                'success': True,
                'deleted': book.id,
                'books': pagination,
                'total_books': len(books)
            })

        except:
            abort(422)
        # for testing DELETE: curl -X DELETE http://127.0.0.1:5000/books/10

    @app.route('/books', methods=['POST'])
    def create_book():

        body = request.get_json()
        new_title = body.get('title', None)
        new_author = body.get('author', None)
        new_rating = body.get('rating', None)

        try:
            book = Book(title=new_title, author=new_author, rating=new_rating)

            book.insert()
            books = Book.query.all()
            pagination = paginate_books(books)

            return jsonify({
                'success': True,
                'created': book.id,
                'books': pagination,
                'total_books': len(books)
            })

        except:
            abort(422)
        # for testing POST: curl -X POST -H "Content-Type: application/json" -d '{"title":"Harry Potter", "author":"Joanne K. Rowling", "rating":"8"}' http://127.0.0.1:5000/books

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
