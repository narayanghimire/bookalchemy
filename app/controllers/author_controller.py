from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.author_service import AuthorService

author_controller = Blueprint('author_controller', __name__, url_prefix='/authors')

author_service = AuthorService()

@author_controller.route('/add', methods=['GET', 'POST'])
def add_author():
    """add new authors"""
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        try:
            # Adding the author using the author service
            author_service.add_author(name, birth_date, date_of_death)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
                return jsonify({'status': 'success', 'message': f'Author "{name}" has been successfully added.'}), 200

            flash(f'Author "{name}" has been successfully added.', 'success')
            return redirect(url_for('home'))  # Redirect to home or relevant page

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check for AJAX request
                return jsonify({'status': 'error', 'message': 'Failed to add author.'}), 500

            flash(f'Failed to add author "{name}".', 'error')
            return redirect(url_for('home'))

# Fetch all authors
@author_controller.route('/', methods=['GET'])
def get_authors():
    """get all authors"""
    authors = author_service.get_all_authors()  # Get all authors from the database
    return jsonify({'authors': [{'id': author.id, 'name': author.name} for author in authors]})
