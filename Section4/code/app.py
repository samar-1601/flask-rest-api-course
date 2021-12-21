# Encounter issue with virtual env and python package problems:
# https://medium.com/swlh/how-to-run-a-different-version-of-python-from-your-terminal-fe744276ff22
# https://stackoverflow.com/questions/48911582/virtualenv-to-path-on-windows-10

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left empty!"
    )

    @jwt_required() # need to authenticate before we call the get() method
    def get(self, name):
        item = next(filter(lambda x: x['name']==name, items), None) # return first item with the given name
        return {'item' : item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name']==name, items), None) is not None :
            return {"message" : f"An item with name '{name}' already exists."}, 400 # bad request
            
        data = Item.parser.parse_args()
        item = {"name":name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None:
            return {'message' : 'Item not found!!'}
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message' : 'Item Deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # data["addition"] will be ignored as above only price can be passed as an argument
        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
    
class ItemList(Resource):
    def get(self):
        return {"items" : items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug= True)