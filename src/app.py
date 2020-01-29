
import os
from flask import Flask, request
from flask_restplus import Api, Resource
from flask import render_template

from flask_jwt_extended import JWTManager, jwt_required
from flask_sqlalchemy import SQLAlchemy

from src.controller.status_controller import api as status_ns
from src.controller.addition_controller import api as add_ns
from src.controller.multiplication_controller import api as multi_ns
from src.controller.login_controller import api as login_ns

from src.dto import AddBookDto, ReadBookDto, UpdateBookDto, DeleteBookDto

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
api.add_namespace(add_ns, path="/api/addition")
api.add_namespace(multi_ns, path="/api/multiplication")
api.add_namespace(AddBookDto.api, path="/api/book/add")
api.add_namespace(ReadBookDto.api, path="/api/book/read")
api.add_namespace(UpdateBookDto.api, path="/api/book/update")
api.add_namespace(DeleteBookDto.api, path="/api/book/delete")


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


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
            book = Book(title=request.json.get("title"))
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
            book = Book.query.filter_by(title=oldtitle).first()
            book.title = newtitle
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


@app.route('/home/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
