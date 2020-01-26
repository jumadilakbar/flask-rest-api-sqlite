from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

@app.route('/api/v1/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'user': User.getAll()
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    return response

@app.route('/api/v1/user/register', methods=['POST'])
def user_add():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User(username=username, email=email, password=password)
        user.save()
        construct = {}
        construct['success'] = True
        construct['message'] = 'Data saved'
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct['success'] = False
        construct['error'] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response

@app.route('/api/v1/user/login', methods=['POST'])
def user_login():
    # print(request.json['username'])
    construct = {}
    try:
        # construct = {}
        email = request.form.get('email')
        password = request.form.get('password')
            
        # user = User(username=username, email=email, password=password)
        user = User.query.filter(User.email==email and User.password==password).first()
        # cek_pass = User.query.filter_by(password=password).first()
        print(user)
        if user == None :
            construct['success'] = True
            construct['mesagge'] = ' Username Or Password Wrong'
        else:
            data=[
                    {
                    "username":user.username,
                    "email":user.email,
                    "user_id":user.user_id
                    }
                ]
            access_token = create_access_token(identity=data)
            construct['success'] = True
            construct['access_token'] = access_token
            construct['authorization'] = 'Bearer'
        response = jsonify(construct)
        response.status_code = HttpStatus.CREATED
    except Exception as e:
        construct['success'] = False
        construct['error'] = str(e)
        response = jsonify(construct)
        response.status_code = HttpStatus.BAD_REQUEST
    return response

@app.route('/api/v1/user/who_me', methods=['GET'])
@jwt_required
def who_me():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

