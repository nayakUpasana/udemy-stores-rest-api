from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column (db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')   # One-to-Many relationship

    # The 'id' parameter would be saved straight to the database but just won't be used when creating or editing items
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    # This method will stay as the classmethod as it returns an object of type ItemModel as opposed to a dictionary
    @classmethod
    def find_by_name(cls, name):
        # '.query' comes with 'db.Model'
        # To filter on multiple things we can add filter_by one after the other or put it one filter_by
        # Eg. ItemModel.query.filter_by(name=name).filter_by(id=1).filter_by(user='customer')
        # OR ItemModel.query.filter_by(name=name, id=1, user='customer')
        # return cls.query      SELECT * FROM items, and we cannot do this since 'query' is a query builder
        # return ItemModel.query.filter_by(name=name)   SELECT * FROM items WHERE name=name, the first 'name' belongs
        # to the column in the table
        return cls.query.filter_by(name=name).first()     # SELECT * FROM items WHERE name=name LIMIT 1

        # Code from sqlite3
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(*row)
        #     # OR return cls(row[0], row[1])

    # def insert(self):
    # With SQLAlchemy, the 'session.add' can handle both the things for inserting and updating, so we don't need
    # a update method
    def save_to_db(self):
        # Unlike sqlite3, SQLAlchemy can convert the object to row values when inserting
        db.session.add(self)
        db.session.commit()

        # Code from sqlite3
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

