from models.acl import AclResource, Privilege
return {
    'Can view USER': current_user.is_allowed(AclResource.USER, Privilege.VIEW),
    'Can add USER': current_user.is_allowed(AclResource.USER, Privilege.ADD),
    'Can update USER': current_user.is_allowed(AclResource.USER, Privilege.UPDATE),
    'Can delete USER': current_user.is_allowed(AclResource.USER, Privilege.DELETE),
    'Can view ADMIN': current_user.is_allowed(AclResource.ADMIN, Privilege.VIEW),
    'Can view SETTINGS': current_user.is_allowed(AclResource.SETTINGS, Privilege.VIEW),
    'Can view PRODUCTS': current_user.is_allowed(AclResource.PRODUCT, Privilege.VIEW),
    'Can view CATEGORIES': current_user.is_allowed(AclResource.CATEGORY, Privilege.VIEW)
}