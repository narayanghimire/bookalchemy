from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.book_service import BookService
from app.services.author_service import AuthorService

book_controller = Blueprint('book_controller', __name__, url_prefix='/books')

book_service = BookService()
author_service = AuthorService()


@book_controller.route('/add', methods=['POST'])
def add_book():
    """add books by authors"""
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        try:
            # Adding the book using the book service
            book_service.add_book(title, isbn, publication_year, author_id)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
                return jsonify({'status': 'success', 'message': f'Book "{title}" has been successfully added.'}), 200

            flash(f'Book "{title}" has been successfully added.', 'success')
            return redirect(url_for('home'))  # Redirect to home or relevant page

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
                return jsonify({'status': 'error', 'message': 'Failed to add book.'}), 500

            flash(f'Failed to add book "{title}".', 'error')
            return redirect(url_for('home'))


@book_controller.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """delete book by book id"""
    try:
        # Attempt to delete the book
        book_service.delete_book(book_id)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
            return jsonify({'status': 'success', 'message': 'Book successfully deleted!'}), 200

        flash('Book successfully deleted!', 'success')
        return redirect(url_for('home'))  # Redirect to home or relevant page

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
            return jsonify({'status': 'error', 'message': 'Failed to delete book.'}), 500

        flash('Failed to delete the book.', 'error')
        return redirect(url_for('home'))  # Redirect to home or relevant page
