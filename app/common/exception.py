#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

class NetworkError(Exception):
	def __init__(self, error, description):
		self.error = error
		self.description = description

	def __repr__(self):
		return 'NetworkError: %s' % self.error
	def __str__(self):
		return '%s. %s' % (self.error, self.description)

class DatabaseError(Exception):
	def __int__(self, error, status_code, message):
		self.error = self.error
		self.status_code = status_code
		self.message = message
	def __repr__(self):
		return 'DatabaseError: %s' %self.error

	def __str__(self):
		return '%s, %s, %s' %(self.error, self.status_code, self.message)