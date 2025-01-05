from app.models.data_models import db, Book


class BookService:
    """
       Service class for handling operations related to Books, such as adding and deleting books.
    """
    def add_book(self, title, isbn, publication_year, author_id):
        " Adds a new book to the database."
        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )
        db.session.add(book)
        db.session.commit()

    def delete_book(self, book_id):
        "Deletes a book from the database and removes the associated author if they have no other books."
        book = Book.query.get_or_404(book_id)
        author = book.author
        db.session.delete(book)
        db.session.commit()

        if not author.books:
            db.session.delete(author)
            db.session.commit()