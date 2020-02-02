
import os
from flask import Flask, request
from flask_restplus import Api, Resource
from flask import render_template

from flask_jwt_extended import JWTManager, jwt_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from src.controller.status_controller import api as status_ns
# from src.controller.addition_controller import api as add_ns
# from src.controller.multiplication_controller import api as multi_ns
from src.controller.login_controller import api as login_ns

from src.dto import AddBookDto, ReadBookDto, UpdateBookDto, DeleteBookDto
from src.dto import AddAuthorDto, ReadAuthorDto, UpdateAuthorDto, DeleteAuthorDto

app_title = 'Template project for Flask'
app_description = 'Showcase project for building Flask micro-service web app.'

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['JWT_TOKEN_LOCATION'] = ['json']
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

jwt = JWTManager(app)
db = SQLAlchemy(app)

api = Api(app=app, title=app_title,
          version='1.0',
          description=app_description)

api.add_namespace(status_ns, path="/status")
api.add_namespace(login_ns, path="/login")
# api.add_namespace(add_ns, path="/api/addition")
# api.add_namespace(multi_ns, path="/api/multiplication")
api.add_namespace(AddBookDto.api, path="/api/book/add")
api.add_namespace(ReadBookDto.api, path="/api/book/read")
api.add_namespace(UpdateBookDto.api, path="/api/book/update")
api.add_namespace(DeleteBookDto.api, path="/api/book/delete")

api.add_namespace(AddAuthorDto.api, path="/api/author/add")
api.add_namespace(ReadAuthorDto.api, path="/api/author/read")
api.add_namespace(UpdateAuthorDto.api, path="/api/author/update")
api.add_namespace(DeleteAuthorDto.api, path="/api/author/delete")


# class User(db.Model):
#     __tablename__ = 'user'
#     username = db.Column(db.String(20), unique=True, primary_key=True)
#     password = db.Column(db.String(20))
#     email = db.Column(db.String(20))
#     date_of_birth = db.Column(db.String(15))
#     # books = relationship('Book', backref='user_books', lazy=True)
#
#     def __repr__(self):
#         return "<Author name: {}, date of birth: {}, nationality: {}, books: {}>".format(
#             self.name, self.date_of_birth, self.nationality, self.books)


class Book(db.Model):
    __tablename__ = 'book'
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String, ForeignKey('author.name'),
                       nullable=False)
    # user = db.Column(db.String, ForeignKey('user.username'),
    #                  nullable=False)
    year = db.Column(db.Integer)
    language = db.Column(db.String(10))

    def __repr__(self):
        return "<Title: {}, author: {}, publish_year: {}, language: {}>".format(
            self.title, self.author, self.year, self.language)


class Author(db.Model):
    __tablename__ = 'author'
    name = db.Column(db.String(20), unique=True, primary_key=True)
    date_of_birth = db.Column(db.String(15))
    nationality = db.Column(db.String(15))
    books = relationship('Book', backref='book_of_author', lazy=True)

    def __repr__(self):
        return "<Author name: {}, date of birth: {}, nationality: {}, books: {}>".format(
            self.name, self.date_of_birth, self.nationality, self.books)


db.create_all()


@AddBookDto.api.route('/')
class AddBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', AddBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Add book to database.')
    @api.expect(AddBookDto.request, validate=True)
    @api.marshal_with(fields=AddBookDto.response)
    def post(self):

        try:

            author_name = request.json.get("author")
            author = Author.query.filter_by(name=author_name).first()

            book = Book(title=request.json.get("title"),
                        year=request.json.get("year"),
                        author=author.name,
                        language=request.json.get("language"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("exception: ", e)
            return {
                "status": "Failed to add book"
            }

        return {
            "status": "Success!"
        }


@ReadBookDto.api.route('/')
class ReadBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', ReadBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Reads books from database.')
    @api.expect(ReadBookDto.request, validate=True)
    @api.marshal_with(fields=ReadBookDto.response)
    def post(self):

        books = Book.query.all()

        return {
            "books": str(books)
        }


@UpdateBookDto.api.route('/')
class UpdateBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', UpdateBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Updates book in database.')
    @api.expect(UpdateBookDto.request, validate=True)
    @api.marshal_with(fields=UpdateBookDto.response)
    def post(self):
        try:
            newtitle = request.json.get("new_title")
            oldtitle = request.json.get("old_title")
            newyear = request.json.get("new_year")
            newauthor = request.json.get("new_author")
            newlanguage = request.json.get("new_language")
            book = Book.query.filter_by(title=oldtitle).first()
            book.title = newtitle
            book.year = newyear
            book.author = newauthor
            book.language = newlanguage
            db.session.commit()
        except Exception as e:
            return {
                "status": "Failed to update book. Old title not found."
            }

        return {
            "status": "Success!"
        }


@DeleteBookDto.api.route('/')
class DeleteBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', DeleteBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Deletes book from database.')
    @api.expect(DeleteBookDto.request, validate=True)
    @api.marshal_with(fields=DeleteBookDto.response)
    def post(self):
        try:

            title = request.json.get("title")
            book = Book.query.filter_by(title=title).first()
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            return {
                "status": "Failed to delete book. Title not found."
            }
        return {
            "status": "Success!"
        }


@AddAuthorDto.api.route('/')
class AddAuthor(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', AddAuthorDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Add author to database.')
    @api.expect(AddAuthorDto.request, validate=True)
    @api.marshal_with(fields=AddAuthorDto.response)
    def post(self):

        try:

            author = Author(
                name=request.json.get('name'),
                date_of_birth=request.json.get('date_of_birth'),
                nationality=request.json.get('nationality')
                # books=Book.query.filter_by(author=request.json.get('name'))
            )

            db.session.add(author)
            db.session.commit()
        except Exception as e:
            print("exception: ", e)
            return {
                "status": "Failed to add author"
            }

        return {
            "status": "Success!"
        }


@ReadAuthorDto.api.route('/')
class ReadAuthor(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', ReadAuthorDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Reads authors from database.')
    @api.expect(ReadAuthorDto.request, validate=True)
    @api.marshal_with(fields=ReadAuthorDto.response)
    def post(self):

        authors = Author.query.all()

        return {
            "authors": str(authors)
        }


@UpdateAuthorDto.api.route('/')
class UpdateAuthor(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', UpdateAuthorDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Updates author in database.')
    @api.expect(UpdateAuthorDto.request, validate=True)
    @api.marshal_with(fields=UpdateAuthorDto.response)
    def post(self):
        try:
            newname = request.json.get("new_name")
            oldname = request.json.get("old_name")
            newdate = request.json.get("new_date_of_birth")
            newnationality = request.json.get("new_nationality")
            author = Author.query.filter_by(name=oldname).first()
            author.name = newname
            author.date_of_birth = newdate
            author.nationality = newnationality
            db.session.commit()
        except Exception as e:
            return {
                "status": "Failed to update author. Old author name not found."
            }

        return {
            "status": "Success!"
        }


@DeleteAuthorDto.api.route('/')
class DeleteAuthor(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', DeleteAuthorDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Deletes author from database.')
    @api.expect(DeleteAuthorDto.request, validate=True)
    @api.marshal_with(fields=DeleteAuthorDto.response)
    def post(self):
        try:

            name = request.json.get("name")
            author = Author.query.filter_by(name=name).first()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            return {
                "status": "Failed to delete author. Name not found."
            }
        return {
            "status": "Success!"
        }


@app.route('/home/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
