#!/usr/bin/env python3
# -*-coding: UTF-8 -*-
#from app.models.user import identity, authenticate

from flask_migrate import Migrate
migrate = Migrate()


from flask_jwt import JWT
from app.common.authentication import identity, authenticate
jwt=JWT(authentication_handler=authenticate, identity_handler=identity)
