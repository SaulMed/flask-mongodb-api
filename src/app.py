from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo.errors import OperationFailure
from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dbmongo"

mongo = PyMongo(app)

#Add new User
@app.route('/users', methods=['POST'])
def create_user():
    try:
        #Receiving data
        username = request.json['username']
        age = request.json['age']
        email = request.json['email']
        password = request.json['password']

        if username and age and email and password:
            hashed_password = generate_password_hash(password)
            idUser = mongo.db.users.insert_one({
                'username':username,'age':age,'email':email,'password':hashed_password
            })
            response = {
                'id': str(idUser),
                'username': username,
                'age': age,
                'email':email,
                'password':hashed_password
            }
            return response
        else:
            {"message":"Please insert all info."}

        print("Request: ",request.json)
        return {"message":"Created."}
    except OperationFailure as err:
        print("Error: ",err)

#Get All Users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()   #Obtener data de DB
    response = json_util.dumps(users)   #Transformar a Json
    return Response(response, mimetype="application/json")  #Indicar al front que se envia un JSON

#Get One User
@app.route('/users/<id>', methods=['GET'])
def get_one_user(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})    #Importante realizar el casteo a ObjectId
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

#Delete One User
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({"message":"The user "+id+" was deleted successffully."})
    return response

#Update One User
@app.route('/users/<id>', methods=["PUT"])
def update_user(id):
    username = request.json['username']
    age = request.json['age']
    email = request.json['email']
    password = request.json['email']

    if username and age and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
        'username': username,
        'age': age,
        'email': email,
        'password': hashed_password
    }})
    response = jsonify({"message":"The user "+id+" was updated successffully."})
    return response

#Route NOT FOUND
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        "message":"Resource NOT found: "+request.url,
        "status":404
    })
    response.status_code = 404
    return response;

if __name__ == "__main__":
    app.run(debug=True)