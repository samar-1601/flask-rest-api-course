# Encounter issue with virtual env and python package problems:
# https://medium.com/swlh/how-to-run-a-different-version-of-python-from-your-terminal-fe744276ff22
# https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from item import Item, ItemList

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'Jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

app.run(port=5000, debug= True)