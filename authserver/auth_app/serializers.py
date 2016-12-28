from rest_framework import serializers


from .models import (
    Application,
    Organization,
    User,
    Role,
    RoleUserOrgAssociation,
    Permission,
    RolePermissionAssociation,
)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'name',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'parent_id',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'date_joined',
        )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'description',
        )


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'name',
            'description',
            'permissions',
        )
