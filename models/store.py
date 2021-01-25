from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Many-to-one relationship, one store can have many items. 'items' here is a list.
    # items = db.relationship('ItemModel')

    # 'lazy = dynamic' takes care of not creating an item object everytime a StoreModel is created and should be done
    # only when an item is added to the store, in order to improve the speed of creation
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # Following return would throw error with 'lazy' parameter
        # return {'name': self.name, 'items': [item.json() for item in self.items]}

        # With 'lazy', the 'self.items' is not longer a list of items but a query builder that has the ability to look
        # into the items table, so we use '.all()' to retrieve all of the items
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

