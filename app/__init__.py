#!/usr/bin/env python3
# -*-coding: UTF-8 -*-
import os

from flask import Flask

from app.config import config
from app.extensions import migrate, jwt

#from app.api import api_blueprint
from app.resources.user import auth_blueprint

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	register_extensions(app)
	register_blueprints(app)
	return app

def register_extensions(app):
	migrate.init_app(app)
	jwt.init_app(app)

def register_blueprints(app):
	app.register_blueprint(auth_blueprint)

