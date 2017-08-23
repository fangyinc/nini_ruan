#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
	ERROR_404_HELP = False
	JWT_SECRET_KEY = os.environ.get('SECRET_KEY')		#JWT key
	JWT_EXPIRATION_DELTA = timedelta(seconds=36000)		#JWT过期时间
	FLASKY_PER_PAGE = 20
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	ENV = 'dev'
	DEBUG = True

class TestingConfig(Config):
	ENV = 'test'
	TESTING = True
	DEBUG = True

class ProductionConfig(Config):
	ENV = 'prod'
	DEBUG = False

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
