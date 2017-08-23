#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
#from app import jwt
from flask import g
from app.common.http import HttpService, HttpMethods
from app.common.errors import  server_error, bad_request, forbidden
from ..database import  CRUDMixin

from app.common.exception import DatabaseError,NetworkError

class User(CRUDMixin):

	url = CRUDMixin.base_url + 'user/'
	def __init__(self, id=None, email=None, username=None, name=None, password=None, authority=None):
		self.id = id
		self.email = email
		self.username = username
		self.name = name
		self.password = password
		self.authority = authority


	@classmethod
	def get_user(cls, user_id=None, username=None, email=None):
		url=cls.url + 'exist'
		method=HttpMethods.get('post')
		data={'id': user_id, 'username': username, 'email': email}
		try:
			my_http = HttpService(url=url, headers=cls.headers, auth=())
			response = my_http.method(method['method'])(js_data=data)
			if response.status_code == method['code']:
				if response.json() == None:	#没有这个用户
					return None
				return cls(**response.json())
			return None
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	def verify_password(self, password):
		url=self.url+'exist'
		data={'username':self.username, 'email':self.email,'password':password}
		method=HttpMethods.get('post')
		try:
			my_http = HttpService(url=url, headers=self.headers, auth=())
			response = my_http.method(method['method'])(js_data=data)
			if response.status_code == method['code']:
				return True
			return False
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	def reset_password(self, new_password):
		pass
	def can(self, permissions):
		pass
	def _update_url(self):
		return self.url +'update'
	def _save_url(self):
		return self.url + 'insert'
	def _delete_url(self):
		return self.url + str(self.id)

	@classmethod
	def _get_all_url(cls):
		super(User, cls)._get_all_url()
		return cls.url + 'getall'

	@classmethod
	def _get_by_id_url(cls):
		super()._get_by_id_url()
		return cls.url + 'querybyid'

	def to_json(self):
		js_user={
			'id': self.id,
			'email': self.email,
			'username': self.username,
			'name': self.name,
			'password': self.password,
			'authority': self.authority
		}
		return js_user

	def __repr__(self):
		return '<User %s>' %self.username
