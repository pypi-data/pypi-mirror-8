import copy

try:
    from guardian.shortcuts import assign_perm
except ImportError:
    def assign_perm(perm_name, group_or_user, obj):
        pass

from .utils import get_permission_name


def assign_object_to_member(group_member, obj, **kwargs):
    """Assign an object to a GroupMember instance object.
    """
    from settings import GROUPS_MANAGER
    if GROUPS_MANAGER['AUTH_MODELS_SYNC'] and \
            group_member.group.django_group and group_member.member.django_user:
        roles_attr = kwargs.get('roles_attr', 'roles')
        permissions = copy.deepcopy(GROUPS_MANAGER['PERMISSIONS'])
        permissions.update(kwargs.get('custom_permissions', {}))
        # owner
        if isinstance(permissions['owner'], dict):
            roles = getattr(group_member, roles_attr).values_list('codename', flat=True)
            owner_perms = []
            for role in list(set(roles).intersection(set(permissions['owner'].keys()))) + ['default']:
                owner_perms += permissions['owner'].get(role, [])
        else:
            owner_perms = permissions['owner']
        for permission in list(set(owner_perms)):
            perm_name = get_permission_name(permission, obj)
            assign_perm(perm_name, group_member.member.django_user, obj)
        # group
        group_perms = permissions.get('group', [])
        for permission in list(set(group_perms)):
            perm_name = get_permission_name(permission, obj)
            assign_perm(perm_name, group_member.group.django_group, obj)
        # groups_upstream
        upstream_groups = [group.django_group for group in group_member.group.get_ancestors()]
        upstream_perms = permissions.get('groups_upstream', [])
        for django_group in upstream_groups:
            for permission in list(set(upstream_perms)):
                perm_name = get_permission_name(permission, obj)
                assign_perm(perm_name, django_group, obj)
        # groups_downstream
        downstream_groups = \
            [group.django_group for group in group_member.group.get_descendants()]
        downstream_perms = permissions.get('groups_downstream', [])
        for django_group in downstream_groups:
            for permission in list(set(downstream_perms)):
                perm_name = get_permission_name(permission, obj)
                assign_perm(perm_name, django_group, obj)
        # groups_siblings
        siblings_groups = [group.django_group for group in group_member.group.get_siblings()]
        siblings_perms = permissions.get('groups_siblings', [])
        for django_group in siblings_groups:
            for permission in list(set(siblings_perms)):
                perm_name = get_permission_name(permission, obj)
                assign_perm(perm_name, django_group, obj)
