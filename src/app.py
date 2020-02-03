
import os
from flask import Flask, request
from flask_restplus import Api, Resource
from flask import render_template

from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKey

from src.controller.status_controller import api as status_ns

from src.dto import AddBookDto, ReadBookDto, UpdateBookDto, DeleteBookDto
from src.dto import AddAuthorDto, ReadAuthorDto, UpdateAuthorDto, DeleteAuthorDto
from src.dto import RegistrationDto, LoginDto, UserInfoDto, UserGetBookDto, UserReturnBookDto

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
engine = create_engine(database_file)

api = Api(app=app, title=app_title,
          version='1.0',
          description=app_description)

api.add_namespace(status_ns, path="/status")

api.add_namespace(RegistrationDto.api, path="/registration")
api.add_namespace(LoginDto.api, path="/login")

api.add_namespace(UserInfoDto.api, path="/api/userInfo")
api.add_namespace(UserGetBookDto.api, path="/api/user/getBook")
api.add_namespace(UserReturnBookDto.api, path="/api/user/returnBook")

api.add_namespace(AddBookDto.api, path="/api/book/add")
api.add_namespace(ReadBookDto.api, path="/api/book/read")
api.add_namespace(UpdateBookDto.api, path="/api/book/update")
api.add_namespace(DeleteBookDto.api, path="/api/book/delete")

api.add_namespace(AddAuthorDto.api, path="/api/author/add")
api.add_namespace(ReadAuthorDto.api, path="/api/author/read")
api.add_namespace(UpdateAuthorDto.api, path="/api/author/update")
api.add_namespace(DeleteAuthorDto.api, path="/api/author/delete")


loans = db.Table('loan',
    db.Column('user_name', db.String, ForeignKey('user.username'), primary_key=True),
    db.Column('book_name', db.String, ForeignKey('book.title'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(15))
    books = relationship('Book', secondary=loans, backref=backref('books', lazy=True), lazy="subquery")

    def __repr__(self):
        return "<Username: {}, password: {}, email: {}, date of birth: {}, loaned books: {}>".format(
            self.username, self.password, self.email, self.date_of_birth, self.books)


class Book(db.Model):
    __tablename__ = 'book'
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String, ForeignKey('author.name'),
                       nullable=False)
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

            if author is not None:
                book_title = request.json.get("title")
                b = Book.query.filter_by(title=book_title).first()

                if b is None:
                    book = Book(title=book_title,
                                year=request.json.get("year"),
                                author=author.name,
                                language=request.json.get("language"))
                    db.session.add(book)
                    db.session.commit()
                else:
                    raise Exception("Book with given name already exists!")
            else:
                raise Exception("Given author not found!")
        except Exception as e:
            return {
                "status": "Failed to add book. Exception: " + str(e)
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
            title = request.json.get("title")
            newyear = request.json.get("new_year")
            newauthor = request.json.get("new_author")
            newlanguage = request.json.get("new_language")

            book = Book.query.filter_by(title=title).first()

            if book is not None:
                book.year = newyear
                book.author = newauthor
                book.language = newlanguage
                db.session.commit()
            else:
                raise Exception("Book with given title does not exist!")
        except Exception as e:
            return {
                "status": "Failed to update book. Exception: " + str(e)
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

            if book is not None:
                db.session.delete(book)
                db.session.commit()
            else:
                raise Exception("Book with given title does not exist!")

        except Exception as e:
            return {
                "status": "Failed to delete book. Exception: " + str(e)
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
            author_name = request.json.get('name')
            a = Author.query.filter_by(name=author_name).first()

            if a is None:
                author = Author(
                    name=author_name,
                    date_of_birth=request.json.get('date_of_birth'),
                    nationality=request.json.get('nationality')
                )

                db.session.add(author)
                db.session.commit()
            else:
                raise Exception("Author with given name already exists!")

        except Exception as e:
            return {
                "status": "Failed to add author. Exception: " + str(e)
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
            name = request.json.get("name")
            newdate = request.json.get("new_date_of_birth")
            newnationality = request.json.get("new_nationality")

            author = Author.query.filter_by(name=name).first()

            if author is not None:
                author.date_of_birth = newdate
                author.nationality = newnationality
                db.session.commit()
            else:
                raise Exception("Author with given name does not exist!")

        except Exception as e:
            return {
                "status": "Failed to update author. Exception: " + str(e)
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
            if author is not None:
                b = Book.query.filter_by(author=author.name).first()
                if b is None:
                    db.session.delete(author)
                    db.session.commit()
                else:
                    raise Exception("Library has a book of this author. Author cannot be deleted!")
            else:
                raise Exception("Author with given name does not exist!")

        except Exception as e:
            return {
                "status": "Failed to delete author. Exception: " + str(e)
            }
        return {
            "status": "Success!"
        }


@RegistrationDto.api.route('/')
class Registration(Resource):
    @api.response(200, 'Successfully Requested', RegistrationDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Add user to database.')
    @api.expect(RegistrationDto.request, validate=True)
    @api.marshal_with(fields=RegistrationDto.response)
    def post(self):

        try:
            username = request.json.get('username')
            u = User.query.filter_by(username=username).first()

            if u is None:
                user = User(
                    username=username,
                    password=request.json.get('password'),
                    email=request.json.get('email'),
                    date_of_birth=request.json.get('date_of_birth')
                )

                db.session.add(user)
                db.session.commit()
            else:
                raise Exception("Username already exists!")

        except Exception as e:
            return {
                "status": "Failed to add user. Exception: " + str(e)
            }

        return {
            "status": "Success!"
        }


@LoginDto.api.route('/')
class Login(Resource):
    @api.response(200, 'Successfully Requested', LoginDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('User login.')
    @api.expect(LoginDto.request, validate=True)
    @api.marshal_with(fields=LoginDto.response)
    def post(self):

        username = request.json.get('username')
        password = request.json.get('password')

        try:
            user = User.query.filter_by(username=username).first()

            if user is not None:
                if user.password == password:
                    access_token = create_access_token(identity=username+password+user.email+user.date_of_birth)
                    return {
                        "status": "Success!",
                        "access_token": access_token
                    }
                else:
                    raise Exception("Incorrect password!")
            else:
                raise Exception("Username not found!")
        except Exception as e:
            return {
                "status": "Error! Exception: " + str(e),
                "access_token": ""
            }


@UserInfoDto.api.route('/')
class UserInfo(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', UserInfoDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('Reads user from database.')
    @api.expect(UserInfoDto.request, validate=True)
    @api.marshal_with(fields=UserInfoDto.response)
    def post(self):

        username = request.json.get('username')

        try:
            user = User.query.filter_by(username=username).first()

            if user is not None:
                return {
                    'status': "Success!",
                    'username': user.username,
                    'password': user.password,
                    'email': user.email,
                    'date_of_birth': user.date_of_birth,
                    'books': str(user.books)
                }
            else:
                raise Exception("Username does not exist!")

        except Exception as e:
            return {
                'status': "Error! Exception: " + str(e),
                'username': "",
                'password': "",
                'email': "",
                'date_of_birth': "",
                'books': ""
            }


@UserGetBookDto.api.route('/')
class UserGetBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', UserGetBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('User gets book from library.')
    @api.expect(UserGetBookDto.request, validate=True)
    @api.marshal_with(fields=UserGetBookDto.response)
    def post(self):

        username = request.json.get('username')
        title = request.json.get('title')

        try:
            user = User.query.filter_by(username=username).first()
            book = Book.query.filter_by(title=title).first()

            if user is not None:
                if book is not None:

                    ins = loans.insert().values(user_name=username, book_name=title)
                    conn = engine.connect()
                    conn.execute(ins)

                    return {
                        'status': "Success! User " + username + " now possess book: " + title
                    }
                else:
                    raise Exception("Book does not exist!")
            else:
                raise Exception("User does not exist!")

        except Exception as e:
            return{
                'status': "Failed to get the book. Exception: " + str(e)
            }


@UserReturnBookDto.api.route('/')
class UserReturnBook(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', UserReturnBookDto.response)
    @api.response(400, 'Bad Request')
    @api.doc('User returns book to library.')
    @api.expect(UserReturnBookDto.request, validate=True)
    @api.marshal_with(fields=UserReturnBookDto.response)
    def post(self):

        username = request.json.get('username')
        title = request.json.get('title')

        try:
            user = User.query.filter_by(username=username).first()
            book = Book.query.filter_by(title=title).first()

            if user is not None:
                if book is not None:

                    ret = loans.delete().where((and_(loans.c.user_name == username, loans.c.book_name == title)))
                    conn = engine.connect()
                    conn.execute(ret)

                    return {
                        'status': "Success! User " + username + " returned book: " + title
                    }
                else:
                    raise Exception("Book does not exist!")
            else:
                raise Exception("User does not exist!")

        except Exception as e:
            return {
                'status': "Failed to return the book. Exception: " + str(e)
            }


@app.route('/home/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
