#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import functools
from flask import g, abort, current_app, request, jsonify, make_response
from app.models.user import  User
from datetime import datetime, timedelta
import jwt
from jwt import DecodeError, ExpiredSignature
from functools import wraps
import json
from .errors import bad_request, unauthorized
#jwt回调函数
def identity(payload):
	user_id = payload['identity']
	user = User.get_by_id(user_id=user_id)
	g.user = user
	return user
#jwt回调函数
def authenticate(username, password):
	user = User.get_user(username=username)
	if user == None:
		'''用户名为空，说明用邮箱验证'''
		user = User.get_user(email=username)
	g.user=user
	if user and user.verify_password(password):
		return user
	return None

def self_only(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if kwargs.get('username', None):
			if g.user.username != kwargs['username']:
				abort(403)
		if kwargs.get('user_id', None):
			if g.user.id != kwargs['user_id']:
				abort(403)
		return func(*args, **kwargs)
	return wrapper

# JWT AUTh process start
def create_token(user):
	payload = {
		'sub': user.id,
		'iat': datetime.utcnow(),
		'exp': datetime.utcnow() + current_app.config['JWT_EXPIRATION_DELTA']
	}
	token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
	return token.decode('unicode_escape')

def get_token_response(**kwargs):
	user = authenticate(kwargs.get('username'), kwargs.get('password'))
	if user is None:
		return unauthorized('invalid　username or password')
	token_value = create_token(user)
	token={}
	token['access_token']= token_value
	exp = {}
	# 从配置文件获取token过期时间
	exp['expiration'] = int((current_app.config.get('JWT_EXPIRATION_DELTA')).total_seconds())
	user = g.user.to_json()
	token.update(exp)  # 添加过期时间dict中
	token.update({'user': user})  # 添加用户信息dict中

	response = make_response(jsonify(token))
	response.status_code = 201
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

def parse_token(req):
	token = req.headers.get('Authorization').split()[1]
	return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not request.headers.get('Authorization'):
			return bad_request('Missing authorization header')
		try:
			payload = parse_token(request)
		except DecodeError:
			return unauthorized('Token is invalid')
		except ExpiredSignature:
			return unauthorized('Token has expired')
		g.user_id = payload['sub']
		g.user =  User.get_by_id(user_id=g.user_id)
		return f(*args, **kwargs)
	return decorated_function
