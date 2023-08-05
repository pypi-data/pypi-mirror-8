# Copyright (c) 2014, Nicolas Vanhoren
# 
# Released under the MIT license
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals, print_function, absolute_import

import sqlalchemy as sa
import datetime
import re
import bcrypt
import asgard

BCRYPT_TURNS = 10

class UsersPlugin(object):
    def __init__(self, app):
        self.app = app
        self.users = sa.Table('users', app.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('email', sa.String(50), nullable=True, unique=True),
            sa.Column('password_hash', sa.String(100), nullable=False),
            sa.Column('creation_date', sa.DateTime(), nullable=False, default=datetime.datetime.now),
        )

        @app.manager
        class UsersManager(asgard.table_manager(self.users)):
            def create_user(self, email, password):
                password = unicode(password).encode("utf8")
                phash = bcrypt.hashpw(password, bcrypt.gensalt(BCRYPT_TURNS))
                return self.create({"email": email, "password_hash": "bcrypt:://" + phash})

            def set_password(self, user_id, password):
                password = unicode(password).encode("utf8")
                phash = bcrypt.hashpw(password, bcrypt.gensalt(BCRYPT_TURNS))
                updated = self.update_by_id(user_id, {"password_hash": "bcrypt:://" + phash})
                return updated

            def test_user(self, email, password):
                password = unicode(password).encode("utf8")
                try:
                    user = self.read_by_email(email, ["password_hash"])
                except asgard.PersistenceException:
                    return False
                phash = re.match("^bcrypt\:\:\/\/(.*)$", user["password_hash"]).group(1)
                phash = unicode(phash).encode("utf8")
                if bcrypt.hashpw(password, phash) == phash:
                    return True
                return False

            def read_by_email(self, email, fields=None):
                users = self.read(["email == :email", {"email": email}], fields)
                if len(users) == 0:
                    raise asgard.PersistenceException("Unknown email: %s" % email)
                return users[0]

        self.UsersManager = UsersManager