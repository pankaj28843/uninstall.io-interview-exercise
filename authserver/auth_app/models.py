from __future__ import unicode_literals

import collections

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import AbstractBaseUser

from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from .managers import UserManager


class Application(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = AutoCreatedField(_('created at'))
    updated_at = AutoLastModifiedField(_('updated at'))
    name = models.CharField(_('name'), max_length=255, unique=True)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        db_table = 'applications'
        verbose_name = _('application')
        verbose_name_plural = _('applications')


class Organization(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = AutoCreatedField(_('created at'))
    updated_at = AutoLastModifiedField(_('updated at'))
    name = models.CharField(_('name'), max_length=255, unique=True)
    parent = models.ForeignKey('Organization', null=True, related_name='children')
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        db_table = 'organizations'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    date_joined = AutoCreatedField(_('date joined'))
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    updated_at = AutoLastModifiedField(_('updated at'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'name',
    )

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return False

    def get_permissions(self):
        roles_ids = RoleUserOrgAssociation.objects.filter(
            user=self,
        ).values_list('role_id', flat=True)

        permissions_ids = RolePermissionAssociation.objects.filter(
            role_id__in=roles_ids,
        ).values_list('permission_id', flat=True)

        permissions = Permission.objects.filter(id__in=permissions_ids).all()

        return permissions

    def get_organizations(self):
        from .serializers import (
            OrganizationSerializer,
            RoleSerializer,
        )

        associated_roles = RoleUserOrgAssociation.objects.filter(
            user=self,
        ).select_related(
            'role',
            'organization',
        ).prefetch_related(
            'role__permissions',
        ).all()

        organizations_dict = collections.defaultdict(dict)
        for associated_role in associated_roles:
            organization = associated_role.organization
            role = associated_role.role

            organizations_dict[organization.id]['obj'] = organization
            try:
                roles = organizations_dict[organization.id]['roles']
            except KeyError:
                roles = organizations_dict[organization.id]['roles'] = []

            roles.append(RoleSerializer(role).data)

        organizations = []
        for _org_dict in organizations_dict.values():
            _org_data = OrganizationSerializer(_org_dict['obj']).data
            _org_data['roles'] = _org_dict['roles']
            organizations.append(_org_data)

        return organizations


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = AutoCreatedField(_('created at'))
    updated_at = AutoLastModifiedField(_('updated at'))
    name = models.CharField(_('name'), max_length=255)
    description = models.CharField(_('description'), max_length=255)
    permissions = models.ManyToManyField('Permission', through='RolePermissionAssociation')

    class Meta:
        db_table = 'roles'
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class RoleUserOrgAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, null=False)
    organization = models.ForeignKey(Organization, null=False)
    user = models.ForeignKey(User, null=False)

    class Meta:
        db_table = 'roles_users_org'
        unique_together = (
            ('role', 'organization', 'user',),
        )
        verbose_name = _('role + user + organization association')
        verbose_name_plural = _('role + user + organization associations')


class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = AutoCreatedField(_('created at'))
    updated_at = AutoLastModifiedField(_('updated at'))
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.CharField(_('description'), max_length=255)
    roles = models.ManyToManyField(Role, through='RolePermissionAssociation')

    class Meta:
        db_table = 'permissions'
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')


class RolePermissionAssociation(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, null=False)
    permission = models.ForeignKey(Permission, null=False)

    class Meta:
        db_table = 'roles_permissions'
        unique_together = (
            ('role', 'permission',),
        )
        verbose_name = _('role + permission association')
        verbose_name_plural = _('role + permission associations')
