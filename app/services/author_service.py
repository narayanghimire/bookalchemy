from app.models.data_models import db, Author
from datetime import datetime

class AuthorService:
    "Service class for handling operations related to Authors, such as adding and fetching authors."
    def add_author(self, name, birth_date, date_of_death):
        "Adds a new author to the database."
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
        date_of_death_obj = datetime.strptime(date_of_death, '%Y-%m-%d').date() if date_of_death else None

        author = Author(
            name=name,
            birth_date=birth_date_obj,
            date_of_death=date_of_death_obj
        )

        db.session.add(author)
        db.session.commit()

    def get_all_authors(self):
        " Retrieves all authors from the database"
        return Author.query.all()
