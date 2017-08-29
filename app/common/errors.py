#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from flask import jsonify, make_response

#请求不可用或不一致
def bad_request(message):
	response = make_response(jsonify({'error': 'bad request', 'message': message}))
	response.status_code = 400
	response.headers['Access-Control-Allow-Origin'] = '*'
	return response

#Unauthorized（ 未授权） 请求未包含认证信息
#或者已经注册但是没有认证的用户
def unauthorized(message):
	response = make_response(jsonify({'error': 'unauthorized', 'message': message}))
	response.status_code = 401
	response.headers['Access-Control-Allow-Origin'] = '*'

	return response

#Forbidden（ 禁止） 请求中发送的认证密令无权访问目标
def forbidden(message):
	response = make_response(jsonify({'error': 'forbidden', 'message': message}))
	response.status_code = 403
	response.headers['Access-Control-Allow-Origin'] = '*'

	return response

def server_error(message):
	response = make_response(jsonify({'error': 'internal server error', 'message': message}))
	response.status_code = 500
	response.headers['Access-Control-Allow-Origin'] = '*'

	return response



errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}
