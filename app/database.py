#!/usr/bin/env python3
#-*- coding:UTF-8 -*-*
import abc
from app.common.http import HttpService, HttpMethods
from app.common.exception import NetworkError, DatabaseError

base_url = 'http://115.29.55.106:8888/'
#base_url = 'http://localhost:5000/api/'

'''
派生类无法覆盖 _func()内部方法
'''

class CRUDMixin(object):
	__metaclass__ = abc.ABCMeta

	base_url = base_url
	headers = {'Content-type':'application/json'}
	@classmethod
	def create(cls, **kwargs):
		'''创建新对象并写入'''
		instance = cls(**kwargs)
		return instance.save()

	def update(self, commit=True, **kwargs):
		'''更新数据'''
		url=self._update_url()

		'''post方法'''
		method=HttpMethods.get('post')

		for attr, value in kwargs.items():
			if value is not None:
				setattr(self, attr, value)
		if not commit:
			return None
		try:
			my_http = HttpService(url=url, headers=self.headers, auth=())
			response = my_http.method(method['method'])(js_data=self.to_json())
			if response.status_code == method['code']:
				#for attr, value in response.json().items():
				#	if value is not None:
				#		setattr(self, attr, value)
				#return response.json()
				'''成功返回True, 否则返回False'''
				return response.json()
			else:
				raise DatabaseError('Invalid upload data', response.status_code, response.text)
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	def save(self, commit=True):
		'''写入数据'''
		url=self._save_url()
		method=HttpMethods.get('post')
		if not commit:
			return None
		try:
			my_http = HttpService(url=url, headers=self.headers, auth=())
			response = my_http.method(method['method'])(js_data=self.to_json())
			if response.status_code == method['code']:
				'''更新数据，注册后数据库服务器返回id'''
				for attr, value in response.json().items():
					if value is not None:
						setattr(self, attr, value)
				return self
			else:
				raise DatabaseError('Invalid upload data', response.status_code, response.text)
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	def delete(self, commit=True):
		'''删除对象'''
		url=self._delete_url()
		method=HttpMethods.get('delete')

		if not commit:
			return None
		try:
			#TODO 此处服务器有问题, 返回的数据不是json
			my_http = HttpService(url=url, headers=self.headers, auth=())
			response = my_http.method(method['method'])()
			return response.json()

		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	@classmethod
	def get_all(cls):

		url=cls._get_all_url()

		method=HttpMethods.get('post')

		try:
			my_http = HttpService(url=url, headers=cls.headers, auth=())
			response = my_http.method(method['method'])()
			if response.status_code == method['code']:
				return response.json()
			return None
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	@classmethod
	def get_by_id(cls, user_id):
		id_str = str(user_id)
		url=cls._get_by_id_url()
		method=HttpMethods.get('post')
		try:
			my_http = HttpService(url=url, headers=cls.headers, auth=())
			response = my_http.method(method['method'])(data=id_str)
			if response.status_code == method['code']:
				return cls(**response.json())
			return None
		except NetworkError as e:
			print(e.args)
			raise DatabaseError(e.error, 500, e.description)

	@abc.abstractmethod	#强制子类重写
	def _update_url(self):
		'''获取更新url，需要子类重写，下同'''
		pass
	@abc.abstractmethod
	def _save_url(self):
		pass
	@abc.abstractmethod
	def _delete_url(self):
		pass

	@classmethod
	@abc.abstractmethod
	def _get_all_url(cls):
		pass
	@classmethod
	@abc.abstractmethod
	def _get_by_id_url(cls):
		pass

	@abc.abstractmethod
	def to_json(self):
		pass


