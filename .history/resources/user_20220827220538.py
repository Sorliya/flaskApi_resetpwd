from flask import Response, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_restful.reqparse import RequestParser
from models import db
from sqlalchemy import asc, desc
import json
from common.utils import *
from models.user import User
from app import app


user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, location='json', required=True)
user_args.add_argument("password", type=str, location='json', required=True)
user_args.add_argument("email", type=str, location='json', required=True)

resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "password": fields.String,
    "email": fields.String
}

class UserApi(Resource):
    """Responsible for user registration
    """
    @marshal_with(resource_fields)
    def get(self):
        data = User.query.order_by(asc(User.id)).all()
        return data
    
    def post(self):
        args = user_args.parse_args()
        hashed_password = generate_hash(password=args['password'])
        with app.app_context():
            user = User(username=args['username'], password=args['password'], email=args['email'])
            db.session.add(user)
            db.session.commit()
        return Response(json.dumps({ 'msg': 'Create user successfully' }), status=200, mimetype='application/json')

    def put(self):
        """Update existing user
        """
        '''user_args.add_argument("id", type=int, location='json', required=True)
        args = user_args.parse_args()
        
        with app.app_context():
            user = User.query.filter(User.id==args['id']).update({
                'username': args['username'], 
                'password': args['password'], 
                'email': args['email']
                })
            db.session.commit()'''
        params = json.loads(request.data.decode('utf-8'))

        for item in params:
            hashed_password = ''

            if item['password']:
                hashed_password = generate_hash(password=item['password'])

            with app.app_context():
                if hashed_password != '':
                    User.query.filter(User.id == item['id']).update({
                        'email': item['email'], 
                        'password': hashed_password, 
                        'username': item['username']
                    })
                else:
                    User.query.filter(User.id == item['id']).update({
                        'email': item['email'], 
                        'username': item['username']
                    })
                    
                try:
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                    return Response(json.dumps({ 'msg': 'Duplicate key already exists' }), mimetype='application/json')

        return Response(json.dumps({ 'msg': 'Update user successfully' }), status=200, mimetype='application/json')

