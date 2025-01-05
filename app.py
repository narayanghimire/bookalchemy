# app.py

from flask import Flask, redirect, render_template, request
import os

from app.controllers.author_controller import author_controller
from app.controllers.book_controller import book_controller

# Initialize the Flask app
app = Flask(__name__)

db_path = os.path.join(os.getcwd(), 'data', 'library.sqlite')
# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PREFERRED_URL_SCHEME'] = 'https'

# Initialize SQLAlchemy
from app.models.data_models import db, Book, Author  # Updated import path
db.init_app(app)

# Create tables if they do not exist
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(author_controller)
app.register_blueprint(book_controller)

# Search and home route
@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page using the 'home.html' template."""
    search_query = request.form.get('search_query')  # Get the search query from the form
    sort_by = request.args.get('sort_by', 'title')  # Get the sort criteria from the URL (default: by title)

    # If there's a search query, filter books based on title or author name
    books_query = Book.query.join(Author)
    if search_query:
        books_query = books_query.filter(
            (Book.title.like(f"%{search_query}%")) |
            (Author.name.like(f"%{search_query}%"))
        )

    # Sort the books based on the 'sort_by' value
    if sort_by == 'author':
        books_query = books_query.order_by(Author.name)
    else:
        books_query = books_query.order_by(Book.title)

    books = books_query.all()  # Execute the query
    return render_template('home.html', books=books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
