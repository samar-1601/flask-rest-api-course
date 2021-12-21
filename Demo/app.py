from flask import Flask, jsonify, request, render_template

stores = [
    {
        'name' : 'My Wonderful Store',
        'items' : [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

#__name__ tells that we are running in a unique place
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name' : request_data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name> 
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message' : 'Store not found'})    


# GET /stores
@app.route('/store')
def get_stores():
    return jsonify({'stores' : stores})

# POST/store/<string:name>/item{name: , price:}
# add new item to a store
@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' : 'Store not found'})


# GET/store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items' : store['items']})
    return jsonify({'message' : 'Store item not found'})   

app.run(port=5000)