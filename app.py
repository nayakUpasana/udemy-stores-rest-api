from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)

# SQLAlchemy database is going to live at the root folder of our project. The 'sqlite' here can be changed to 'mysql'
# or 'postgres' etc. depending on what we use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# In order to know when an object had changed but not saved to the database, the tracker comes in handy for that.
# Here we are turning off the tracker for Flask-SQLAlchemy not SQLAlchemy's tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'moon'
api = Api(app)


# Here we tell SQLAlchemy to create the database and the tables as well
# This decorator affects the method below it and runs the method before the first request, no matter what request,
# comes into this app
@app.before_first_request
def create_tables():
    # This will create the 'data.db' file. It's important to have all the imports in place. When importing 'Store' class
    # from the store file, it also sees 'StoreModel' and it goes in to see the table definition, that's how it creates
    # the 'stores' table even when we are not importing it directly in 'app' file. Same goes for the 'users' and
    # 'items' table
    db.create_all()


jwt = JWT(app, authenticate, identity)      # /auth

api.add_resource(Item, '/item/<string:name>')     # http://127.0.0.1:5000/item/piano
api.add_resource(ItemList, '/items')    # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')     # http://127.0.0.1:5000/register
api.add_resource(Store, '/store/<string:name>')     # http://127.0.0.1:5000/store/target
api.add_resource(StoreList, '/stores')      # http://127.0.0.1:5000/stores


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
