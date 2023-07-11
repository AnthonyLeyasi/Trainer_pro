from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Trainer:
    db = "group_project"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.city = data['city']
        self.gym = data['gym']
        self.description = data['description']
        # self.title = data['title']
        # self.picture = data['picture']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []



    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM trainers LEFT JOIN users ON trainers.user_id = users.id;
        """
        result = connectToMySQL(cls.db).query_db(query)
        print(result)  # Add this print statement
        if not result:
            return None
        trainer_list = []
        for row in result:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            trainer_data = {
                "id": row["id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "city": row["city"],
                "gym": row["gym"],
                "description": row["description"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user": user_data,
            }
            trainer = cls(trainer_data)
            trainer_list.append(trainer)
        return trainer_list
















    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM trainers JOIN users on trainers.user_id = users.id WHERE trainers.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(id)
        return cls(results[0])






    @classmethod
    def update(cls, form_data):
        query = "UPDATE trainers SET first_name=%(first_name)s, last_name=%(last_name)s,city=%(city)s,gym=%(gym)s,description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trainers WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO trainers (first_name, last_name, user_id, city, gym, description, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(user_id)s, %(city)s, %(gym)s, %(description)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_trainer(form_data):
        is_valid = True

        if len(form_data['first_name']) < 3:
            flash("First name must be at least 3 characters long.")
            is_valid = False

        if len(form_data['last_name']) < 3:
            flash("Last name must be at least 3 characters long.")
            is_valid = False

        if len(form_data['city']) < 3:
            flash("City must be at least 3 characters long.")
            is_valid = False

        if len(form_data['gym']) < 3:
            flash("Gym must be at least 3 characters long.")
            is_valid = False

        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False

        # if len(form_data['posting']) < 3:
        #     flash("Post must be at least 3 characters long.")
        #     is_valid = False

        return is_valid
