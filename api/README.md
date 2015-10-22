# flask-restful

* View docker machines: 
> docker-machine ls
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM
default   *        virtualbox   Running   tcp://192.168.99.100:2376   

* View docker machine's IP:
> docker-machine ip default

* Build project
> docker-compose build

* Start containers:
> docker-compose run web

* Run migrations:
> docker-compose run web python /var/www/app/migrations.py db migrate

* Database Migrations:
> python migrations.py db revision --autogenerate -m 'Your message goes here' --version-path '1.0'
> OR: python migrations.py db migrate

* Prepare OAuth2 tables
```python
class Client(db.Model):
    __tablename__ = 'client'
    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required

    user_id = db.Column(guid(), db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    user = db.relationship('User')

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        return [
            'email'
        ]
        # if self._default_scopes:
        #     return self._default_scopes.split()
        # return []


class Grant(db.Model):
    __tablename__ = 'grant'
    id = db.Column(db.String(40), primary_key=True)

    user_id = db.Column(guid(), db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    user = db.relationship('User', remote_side=user_id, backref='grants')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        from flask import current_app as app
        session = app.db.session
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def validate_redirect_uri(self, redirect_uri):
        return True


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(
        db.String(40),
        db.ForeignKey('client.client_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )

    client = db.relationship('Client')

    user_id = db.Column(
        guid(),
        db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        from flask import current_app as app
        session = app.db.session
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
```

* Prepare ACL tables
```python
class AclRole(db.Model):
    __tablename__ = 'acl_role'
    id = db.Column(guid(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    parent_id = db.Column(guid(), db.ForeignKey(
        'acl_role.id',
        name='fk_acl_role_id_acl_role',
        ondelete='CASCADE',
        onupdate='CASCADE'
    ), index=True)
    parent = db.relationship('AclRole')

    def get_parents(self):
        """

        :return: array of role.id
        """
        if not self.parent_id:
            return []

        results = [self.parent_id]

        # Include parent's parent
        parent = self.query.filter_by(id=self.parent_id).first()
        results.extend(parent.get_parents())

        return results

    @staticmethod
    def get_default_role():
        from flask import current_app as app
        result = AclRole.query.filter_by(name=app.config.get('DEFAULT_USER_ROLE')).first()
        if not result:
            from sqlalchemy.exc import DataError
            raise DataError('System is missing DEFAULT_ROLE')
        return result

    @staticmethod
    def get_owner_role():
        from flask import current_app as app

        result = AclRole.query.filter_by(name=app.config.get('OWNER_USER_ROLE')).first()
        if not result:
            from sqlalchemy.exc import DataError
            raise DataError('System is missing OWNER_ROLE')

        return result


class AclRoleResource(db.Model):
    __tablename__ = 'acl_role_resource'

    role_id = db.Column(
        guid(),
        db.ForeignKey(
            'acl_role.id',
            name='fk_acl_role_resource_id_acl_role',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    role = db.relationship('AclRole')
    resource_name = db.Column(db.String(255), primary_key=True, nullable=False)
    _privilege = db.Column(db.Integer, name='privilege', primary_key=True, autoincrement=False,
                           nullable=False)
    _permission = db.Column(db.Integer, name='permission', primary_key=True,
                            autoincrement=False, nullable=False)

    @property
    def privilege(self):
        from libraries.bitwise import Bitwise
        return Bitwise(self._privilege)

    @privilege.setter
    def privilege(self, bit):
        self._privilege = bit

    @property
    def permission(self):
        from libraries.bitwise import Bitwise
        return Bitwise(self._permission)

    @permission.setter
    def permission(self, bit):
        self._permission = bit

    @staticmethod
    def get_permission_for_user(user_id, resource_name, privilege, is_owner):
        from sqlalchemy import and_, or_
        from sqlalchemy.sql.operators import in_op

        roles = AclUserRole.get_roles_for(user_id=user_id, is_owner=is_owner)

        return AclRoleResource.query.filter(and_(
            or_(
                AclRoleResource.resource_name == '*',
                AclRoleResource.resource_name == resource_name,
            ),
            AclRoleResource._privilege.op('&')(privilege) > 0,
            in_op(AclRoleResource.role_id, roles)
        )).all()


class AclUserResource(db.Model):
    __tablename__ = 'acl_user_resource'

    user_id = db.Column(
        guid(),
        db.ForeignKey(
            'user.id',
            name='fk_acl_user_resource_id_user',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )

    user = db.relationship('User')
    resource_id = db.Column(guid(), primary_key=True, nullable=False)
    resource_type = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    _privilege = db.Column(db.Integer, name='privilege', primary_key=True, autoincrement=False,
                           nullable=False)
    _permission = db.Column(db.Integer, name='permission', primary_key=True,
                            autoincrement=False, nullable=False)

    @property
    def privilege(self):
        from libraries.bitwise import Bitwise
        return Bitwise(self._privilege)

    @privilege.setter
    def privilege(self, bit):
        self._privilege = bit

    @property
    def permission(self):
        from libraries.bitwise import Bitwise
        return Bitwise(self._permission)

    @permission.setter
    def permission(self, bit):
        self._permission = bit

    @staticmethod
    def get_permission_for_user(user_id, resource_id, resource_type, privilege):
        from sqlalchemy import and_, or_
        return AclUserResource.query.filter(and_(
            AclUserResource.user_id == user_id,
            AclUserResource.resource_id == resource_id,
            or_(
                resource_type is None,
                AclUserResource.resource_type == resource_type
            ),
            AclUserResource._privilege.op('&')(privilege) > 0,
        )).all()


class AclUserRole(db.Model):
    __tablename__ = 'acl_user_role'
    user_id = db.Column(
        guid(),
        db.ForeignKey(
            'user.id',
            name='fk_acl_user_role_id_user',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    user = db.relationship('User')

    role_id = db.Column(
        guid(),
        db.ForeignKey(
            'acl_role.id',
            name='fk_acl_user_role_id_acl_role',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    role = db.relationship('AclRole')

    @staticmethod
    def get_roles_for(user_id, is_owner):
        """

        :param user_id:
        :return: arrays of role.id
        """
        default_role = AclRole.get_default_role()
        results = [default_role.id]

        if is_owner:
            owner_role = AclRole.get_owner_role()
            results.append(owner_role.id)

        roles = AclUserRole.query.filter_by(user_id=user_id).all()

        for r in roles:
            # Add role.id
            results.append(r.role_id)
            if not r.role.parent_id:
                continue

            # Find parent recursive
            results.extend(r.role.get_parents())

        return filter(None, set(results))

```

* Get access_token:
> http://0.0.0.0:5000/oauth/token
> curl -X POST -H "Cache-Control: no-cache" -H "Postman-Token: 2de4306e-efe4-794a-9bcb-9498942cdbc9"
  -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
  -F "grant_type=authorization_code"
  -F "client_secret=WGSYGQZUVYAWXLPRCOMKPCAAGUMHAFQMXQLNIYSOESANOPJCMAUZFUX"
  -F "client_id=CLKDKCBNAXDNVXNJQTCVGXWEAFSWVZLUEVHKGGOZ"
  -F "code=Gbu57qoghGxq79Oolkuh0iuia6xgTn" 'http://0.0.0.0:5000/oauth/token'

> {
  "token_type": "Bearer",
  "version": "0.1.0",
  "access_token": "V4cTidBz278yc8MGPNyoLKYhX6NgtV",
  "scope": "email",
  "expires_in": 3600,
  "refresh_token": "hz8ZrGxQitu6CnqHUsNg5SRQFpMiex"
}

* Or get access_token by refresh_token:
> curl -X POST -H "Cache-Control: no-cache" -H "Postman-Token: 85a594e7-4a06-9b8b-ec17-e6ac66db5390"
  -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
  -F "grant_type=refresh_token"
  -F "client_secret=WGSYGQZUVYAWXLPRCOMKPCAAGUMHAFQMXQLNIYSOESANOPJCMAUZFUX"
  -F "client_id=CLKDKCBNAXDNVXNJQTCVGXWEAFSWVZLUEVHKGGOZ"
  -F "refresh_token=hz8ZrGxQitu6CnqHUsNg5SRQFpMiex"
  'http://0.0.0.0:5000/oauth/token'

> {
  "token_type": "Bearer",
  "version": "0.1.0",
  "access_token": "V4m8F5OR10xV3VJB4fkZpJ5n6VBGNy",
  "scope": "email",
  "expires_in": 3600,
  "refresh_token": "JSjHJ4qtRZedc3W0h0gnD73ZWTHTQ4"
}

* Get endpoint:
> http://<docker_container_ip>:80/api/v1.0/products