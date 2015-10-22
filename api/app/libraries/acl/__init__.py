__author__ = 'gia'
__all__ = [
    'Permission',
    'AclManager',
    'AclRoleResource',
    'AclUserResource',
    'AclRole',
    'AclUserRole'
]

class Permission:
    def __init__(self):
        pass

    ALLOW = 1
    DENIED = 2


class AclManager:
    def __init__(self, user_resource=None, role_resource=None):
        self._acl_user_resource = user_resource
        self._acl_role_resource = role_resource
        pass

    def is_allowed(self, user, resource, privilege):
        """
        :param user:models.EntityBase
        :param resource:
        :param privilege:VIEW|ADD|UPDATE|DELETE
        :return: bool
        """

        user_id = hasattr(user, 'id') and getattr(user, 'id') or user
        resource_type = hasattr(resource, 'resource_type') and getattr(resource, 'resource_type') or resource
        resource_id = hasattr(resource, 'id') and getattr(resource, 'id') or None

        permissions = None
        # Permissions that set on _acl_user_role will overwrite all other permissions
        if resource_id:
            permissions = self._acl_user_resource.get_permission_for_user(
                user_id=user_id,
                resource_id=resource_id,
                resource_type=resource_type,
                privilege=privilege
            )

        # Check permission based on user roles
        if permissions is None:
            created_by_id = (hasattr(resource, 'created_by_id') and getattr(resource, 'created_by_id')) or None
            owner_id = (hasattr(resource, 'owner_id') and getattr(resource, 'owner_id')) or None
            author_id = (hasattr(resource, 'author_id') and getattr(resource, 'author_id')) or None

            permissions = self._acl_role_resource.get_permission_for_user(
                user_id=user_id,
                resource_name=resource_type,
                privilege=privilege,
                is_owner=created_by_id == user_id or owner_id == user_id or author_id == user_id
            )

        if permissions is None or not len(permissions):
            return False

        # Check if there is any denied
        for p in permissions:
            if not hasattr(p, 'permission'):
                raise AttributeError('Object does not have "permission" attribute')

            permission = getattr(p, 'permission')
            if permission.has(Permission.DENIED):
                return False

        return True
