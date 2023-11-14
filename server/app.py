#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    
    def get(self):
        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }
        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response
api.add_resource(Index, '/')
    
class Newsletters(Resource):
    
    def get(self):
        response_dict_list = [i.to_dict() for i in Newsletter.quary.all()]
        response = make_response(jsonify(response_dict_list), 200)
        return response
    
    def post(self):
        new_record = Newsletter(
            title = request.form['title']
            body = request.form['body']
        )
        db.session.add(new_record)
        db.session.commit()
        
        response = make_response(jsonify(new_record), 201)
        return response
api.add_resource(Newsletters, '/newsletters')


class NewslettersID(Resource):
    def get(self, id):
        response_dict = Newsletters.quary.filter_by(id=id).first()
        response = make_response(jsonify(response_dict), 201)
        return response

api.add_resource(Newsletters, '/newsletters/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
