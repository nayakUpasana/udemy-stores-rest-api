from db import db


# It tells the SQLAlchemy that the UserModel and ItemModel are that things that is going to be saved in a database
# and retrieved from the database. It's going to be create a mapping between the database and the objects.
class UserModel(db.Model):
    # Telling the SQLAlchemy the table name where these models are going to be stored
    __tablename__ = 'users'

    # Defining the columns for 'users' table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # The properties should be the same as the defined columns, else it won't be saved in the database.
    # The '_id' was removed since, SQLAlchemy creates one for us and we don't need to specify separately
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

# The UserModel here is an API, not an REST API, with the two methods as the endpoints
