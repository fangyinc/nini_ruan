#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from flask import abort, g, jsonify, request, current_app
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_jwt import JWT, jwt_required
from app.resources.user import auth, link_fields, meta_fields
from app.models.user import User
from app import jwt
import json
from app.common.authentication import self_only
from app.common.authentication import get_token_response, login_required

#from .decorators import login_required
from app.helpers import paginate

'''基本请求解析'''
user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')

'''注册信息请求解析'''
user_register_parser = user_parser.copy()
user_register_parser.add_argument('email')
user_register_parser.add_argument('name')


'''完整请求解析'''
user_full_parser = user_register_parser.copy()
user_full_parser.add_argument('id')
user_full_parser.add_argument('authority')


'''给Web客户端返回的数据'''
user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'email': fields.String,
	'name': fields.String,
}

'''用户集合'''
user_collection_fields = {
	'items': fields.List(fields.Nested(user_fields)),
	'meta': fields.Nested(meta_fields),
}


class TestResource(Resource):
	#method_decorators = [jwt_required()]
	@login_required
	@marshal_with(user_fields)
	def get(self, user_id=None):
		user = User.get_by_id(user_id)
		if not user:
			abort(404)
		return user

	#@marshal_with(user_fields)
	def post(self):
		#print('g.user: ',g.user)
		#g.user.update(**user_parser.parse_args())
		#return g.user
		data = user_parser.parse_args()
		token = get_token_response(**data)
		#print(request.json)
		return token

#CUDM
class UserResource(Resource):

	@login_required
	@marshal_with(user_fields)
	def get(self, user_id=None):
		user = User.get_by_id(user_id)
		if user is not None:
			return user, {'Access-Control-Allow-Origin': '*'}
		abort(404)

	@marshal_with(user_fields)
	def post(self):
		'''用户注册'''
		user = User.create(**user_register_parser.parse_args())
		return user, 201, {'Access-Control-Allow-Origin': '*'}

	#@jwt_required()
	@login_required
	@self_only
	def put(self):
		'''
		修改用户信息，　需要登录
		采用JWT token 验证
		headers={'Authorization':'jwt token_string'}	#内容：　'jwt' + 空格 + token_string
		:param user_id: 用户id
		:return:	返回修改后用户
		'''
		status = g.user.update(**user_register_parser.parse_args())
		if status:
			return {}, 200, {'Access-Control-Allow-Origin': '*'}
		return {}, 401, {'Access-Control-Allow-Origin': '*'}

	#@jwt_required()
	@login_required
	@self_only
	def delete(self):
		'''用户删除'''
		status = g.user.delete()
		if status:
			return {}, 200, {'Access-Control-Allow-Origin': '*'}
		return {}, 401, {'Access-Control-Allow-Origin': '*'}


	#method_decorators = [jwt_required()]

	#获取用户信息



class UserCollectionResource(Resource):
	#@marshal_with(user_collection_fields)
	#@paginate()
	def get(self):
		print('hello')
		users = User.get_all()
		print(users)
		return users

	@marshal_with(user_fields)
	def post(self):
		'''
		用户注册
		:return:
		'''
		user = User.create(**user_register_parser.parse_args())
		print(user.to_json())
		return user, 201

class UserAdminResource(Resource):
	@marshal_with(user_fields)
	def get(self):
		'''
		用户查询 get方法
		:param user_id: 用户id查询
		:param http get data {'username':'', 'email':''}　＃带参数的get查询
		:return: 若有则返回用户，　否则返回
		'''
		data = user_full_parser.parse_args()
		username = data.get('username')
		if username is not None:
			return User.get_user(username=username), {'Access-Control-Allow-Origin': '*'}
		email = data.get('email')
		if email is not None:
			return User.get_user(email=email), {'Access-Control-Allow-Origin': '*'}
		#abort(404)
	#获取JWT toke
	def post(self):
		'''
		获取JWT toke
		post json body:{'username':'', 'password': ''}	#
		:return: response of token
		:retype
		{
			'access_token': '',			#jwt token
			 'expiration': ''			#过期时间(s)
			 'user': {

			 }
		}
		curl 示例：
		$ curl  -H "Content-Type: application/json" \
		$ > -X POST  --data '{"username":"1000test3","password":"test3"}'  \
		$ > http://localhost:5000/auth/users/token

		python requests示例:
		r = requests.post(url, headers={'Content-Type': 'application/json'}, \
			json={"username":"1000test3","password":"test3"})

		'''
		#print(request.headers)
		#token_raw_res=jwt.auth_request_callback()
		#token = json.loads(token_raw_res.get_data().decode('utf-8'))	#获取dict token

		data = user_parser.parse_args()
		token_response = get_token_response(**data)
		return token_response

#用户增删查改
auth.add_resource(UserResource, '/users', '/users/<int:user_id>')
auth.add_resource(UserAdminResource, '/users/token', '/users/query')

auth.add_resource(UserCollectionResource, '/users／query/all')
auth.add_resource(TestResource, '/test')

#auth.make_response({'Access-Control-Allow-Origin': '*'})