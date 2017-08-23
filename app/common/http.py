#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from .exception import NetworkError


'''http方法及其响应码'''
HttpMethods={
	'get': {
		'method': 'get',
		'code': 200
	},
	'post':{
		'method': 'post',
		'code': 200			#上游服务器post返回状态码
	},
	'put':{
		'method': 'put',
		'code': 204
	},
	'delete':{
		'method': 'delete',
		'code': 204
	}
}

class HttpService(object):
	'''
	http请求类,提供四个http方法：post put, get, delete
	传递http方法给method方法返回对应的函数对象,以此调用http方法
	'''
	def __init__(self, url, headers, auth):
		'''
		:param url: 请求地址
		:param headers: 请求头
		:param auth: 认证(二元组）-> (username, password)
		'''
		self.url = url
		self.headers = headers
		self.auth = auth

	def method(self, method):
		'''返回对应的http方法'''
		if method == 'post':
			return self.post_data
		elif method == 'get':
			return self.get_data
		elif method == 'put':
			return self.put_data
		elif method == 'delete':
			return self.delete_data
		else:
			raise NetworkError('Invalid Http method', 'no http method name: %s'%method)
	def post_data(self, data=None, js_data=None):
		'''
		post方法
		:param data: dict字典
		:param js_data: json数据
		:return:		成功连接中心服务器接收到数据为status为：sucess
		:return:		返回值response为requests response对象
		:return:		未成功建立链接status则为: error, 测试response为None
		'''
		try:
			response = requests.post(self.url, headers=self.headers,
									 auth=self.auth,  data=data, json=js_data)
			return response
		except requests.ConnectionError as e:		#网络问题（如：DNS 查询失败、拒绝连接)
			raise NetworkError('Invalid HttpService', 'ConnectionError')
		except requests.Timeout as e:				#请求超时
			raise NetworkError('Invalid HttpService', 'Timeout')
	def put_data(self, data=None, js_data=None):
		'''
		post方法
		:param data: dict字典
		:param js_data: json数据
		:return:		成功连接中心服务器接收到数据为status为：sucess
		:return:		返回值response为requests response对象
		:return:		未成功建立链接status则为: error, 测试response为None
		'''
		try:
			response = requests.put(self.url, headers=self.headers,
									 auth=self.auth,  data=data, json=js_data)
			return response
		except requests.ConnectionError as e:		#网络问题（如：DNS 查询失败、拒绝连接)
			raise NetworkError('Invalid HttpService', 'ConnectionError')
		except requests.Timeout as e:				#请求超时
			raise NetworkError('Invalid HttpService', 'Timeout')
	def get_data(self):
		try:
			response = requests.get(self.url, headers=self.headers,
									 auth=self.auth)
			return response
		except requests.ConnectionError as e:		#网络问题（如：DNS 查询失败、拒绝连接)
			raise NetworkError('Invalid HttpService', 'ConnectionError')
		except requests.Timeout as e:				#请求超时
			raise NetworkError('Invalid HttpService', 'Timeout')
	def delete_data(self):
		try:
			response = requests.delete(self.url, headers=self.headers,
									 auth=self.auth)
			return response
		except requests.ConnectionError as e:		#网络问题（如：DNS 查询失败、拒绝连接)
			raise NetworkError('Invalid HttpService', 'ConnectionError')
		except requests.Timeout as e:				#请求超时
			raise NetworkError('Invalid HttpService', 'Timeout')
