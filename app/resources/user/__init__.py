#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource, reqparse, fields


auth_blueprint = Blueprint("auth", __name__, url_prefix='/auth')
auth = Api(auth_blueprint)

# Marshaled fields for links in meta section
link_fields = {
    'prev': fields.String,
    'next': fields.String,
    'first': fields.String,
    'last': fields.String,
}

# Marshaled fields for meta section
meta_fields = {
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'pages': fields.Integer,
    'links': fields.Nested(link_fields)
}

from . import user
