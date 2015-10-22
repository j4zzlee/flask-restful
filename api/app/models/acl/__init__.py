__author__ = 'gia'
__all__ = [
    'Privilege',
    'AclResource',
    'acl_manager'
]


class Privilege:
    def __init__(self):
        pass

    VIEW = 1
    ADD = 2
    UPDATE = 4
    DELETE = 8


class AclResource:
    def __init__(self):
        pass

    # Modules
    CATEGORY = 'category'
    PRODUCT = 'product'
    ADMIN = 'admin'
    SETTINGS = 'settings'
    USER = 'user'


from libraries.acl import AclManager
from models import AclUserResource, AclRoleResource
acl_manager = AclManager(AclUserResource(), AclRoleResource())
