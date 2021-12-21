import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = []
class Item(Resource):
    # parser so that only a specific key of the entered json goes inside the code
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field cannot be left empty!"
    )
    @jwt_required() # need to authenticate before we call the get() method
    def get(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items where name = ?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}
        return {'message' : 'Item not found'}, 404

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
