#6D/19090072/Muhammad Shuro Fadhillah
#6D/19090118/Ramadhani Fauzi Azhar

# from crypt import methods
from fileinput import filename
import json
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
import datetime


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

# Konfigurasi DB
filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'tokenusers'

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

db.create_all()
# Membuat username admin
dataModel = AuthModel(username='admin', password='admin')
db.session.add(dataModel)
db.session.commit()



# Routing login
class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')
        
        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            token = jwt.encode({"username":queryUsername, "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({"msg":"Login Sukses", "token":token}), 200)
        return jsonify({"msg":"Login Gagal, Silahkan Coba Lagi!"})

#API
api.add_resource(LoginUser, "/api/login", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
