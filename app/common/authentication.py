#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import functools
from flask import g, abort
from app.models.user import  User

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
