from django.db import transaction

from auth_app.models import (
    Application,
    Organization,
    Role,
    Permission,
    User,
    RoleUserOrgAssociation,
    RolePermissionAssociation,
)


def initialize_data():
    clinic = Organization(
        name='ABC Clinic Group',
    )
    clinic.save()

    branch_1 = Organization(
        name='ABC Clinic, Indiranagar Branch, Bengaluru',
        parent=clinic,
    )
    branch_1.save()

    branch_2 = Organization(
        name='ABC Clinic, Koramangala Branch, Bengaluru',
        parent=clinic,
    )
    branch_2.save()

    branch_3 = Organization(
        name='ABC Clinic, MG Road Branch, Bengaluru',
        parent=clinic,
    )
    branch_3.save()

    roles_data = [
        {
            'name': 'Super-Admin',
            'description': 'Can access everything in system and create, modify and delete records as long as the operation keeps database integrity.',
        },
        {
            'name': 'Group-Owner',
            'description': 'Owns a group of clinic branches',
        },
        {
            'name': 'Clinic-Owner',
            'description': 'Owns a Clinic branch',
            'permissions': [
                'Patient-GET',
                'Patient-POST',
                'Patient-PUT',
                'Patient-PATCH',
                'Patient-DELETE',
            ],
        },
        {
            'name': 'Clinic-Assistant',
            'description': 'An admin who can only make and change appointments in a branch.',
            'permissions': [
                'Patient-GET',
            ],
        },
        {
            'name': 'Clinic-Doctor',
            'description': 'A doctor who works in one or more branche of a clinic group.',
            'permissions': [
                'Patient-GET',
                'Patient-POST',
                'Patient-PUT',
                'Patient-PATCH',
            ],
        },
        {
            'name': 'Mobile-Patient',
            'description': 'Any patient who uses the mobile to use our services (appointment, chat etc).',
            'permissions': [
                'Patient-GET',
                'Patient-PUT',
                'Patient-PATCH',
            ],
        },
        {
            'name': 'Chat-Doctor',
            'description': 'Any doctor who uses the mobile to provide chat services.',
            'permissions': [
                'Patient-GET',
                'Patient-POST',
                'Patient-PUT',
                'Patient-PATCH',
                'Patient-DELETE',
            ],
        },
    ]

    roles_obj_dict = {}

    for data in roles_data:
        role = Role(
            name=data['name'],
            description=data['description'],
        )
        role.save()
        roles_obj_dict[role.name] = role

        permission_names = data.get('permissions', [])

        for name in permission_names:
            try:
                permission_obj = Permission.objects.get(name__iexact=name)
            except Permission.DoesNotExist:
                permission_obj = Permission(
                    name=name,
                )
                permission_obj.save()

            RolePermissionAssociation.objects.get_or_create(role=role, permission=permission_obj)

    super_admin_user = User.objects.create_superuser(
        'admin@awesomehealthapp.com',
        'password',
        name='Super Admin User',
    )

    doctor_1_user = User.objects.create_user(
        'doctor1@abcclinic.com',
        'password',
        name='Doctor 1',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_1_user,
        role=roles_obj_dict['Clinic-Doctor'],
        organization=branch_1,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_1_user,
        role=roles_obj_dict['Chat-Doctor'],
        organization=branch_1,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_1_user,
        role=roles_obj_dict['Clinic-Doctor'],
        organization=branch_2,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_1_user,
        role=roles_obj_dict['Chat-Doctor'],
        organization=branch_2,
    )

    doctor_2_user = User.objects.create_user(
        'doctor2@abcclinic.com',
        'password',
        name='Doctor 2',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_2_user,
        role=roles_obj_dict['Clinic-Doctor'],
        organization=branch_2,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_2_user,
        role=roles_obj_dict['Chat-Doctor'],
        organization=branch_2,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_2_user,
        role=roles_obj_dict['Clinic-Doctor'],
        organization=branch_3,
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=doctor_2_user,
        role=roles_obj_dict['Chat-Doctor'],
        organization=branch_3,
    )

    group_owner_user = User.objects.create_user(
        'groupowner@abcclinic.com',
        'password',
        name='ABC Clinic Group Owner',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=group_owner_user,
        role=roles_obj_dict['Group-Owner'],
        organization=clinic,
    )

    branch_1_owner_user = User.objects.create_user(
        'Indiranagar@abcclinic.com',
        'password',
        name='ABC Clinic Indiranagar Branch Owner',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_1_owner_user,
        role=roles_obj_dict['Clinic-Owner'],
        organization=branch_1,
    )

    branch_2_owner_user = User.objects.create_user(
        'Koramangala@abcclinic.com',
        'password',
        name='ABC Clinic Koramangala Branch Owner',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_2_owner_user,
        role=roles_obj_dict['Clinic-Owner'],
        organization=branch_2,
    )

    branch_3_owner_user = User.objects.create_user(
        'MGRoad@abcclinic.com',
        'password',
        name='ABC Clinic MGRoad Branch Owner',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_3_owner_user,
        role=roles_obj_dict['Clinic-Owner'],
        organization=branch_3,
    )

    branch_1_assistant_user = User.objects.create_user(
        'IndiranagarAssistant@abcclinic.com',
        'password',
        name='ABC Clinic Indiranagar Branch Assistant',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_1_assistant_user,
        role=roles_obj_dict['Clinic-Assistant'],
        organization=branch_1,
    )

    branch_2_assistant_user = User.objects.create_user(
        'KoramangalaAssistant@abcclinic.com',
        'password',
        name='ABC Clinic Koramangala Branch Assistant',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_2_assistant_user,
        role=roles_obj_dict['Clinic-Assistant'],
        organization=branch_2,
    )

    branch_3_assistant_user = User.objects.create_user(
        'MGRoadAssistant@abcclinic.com',
        'password',
        name='ABC Clinic MGRoad Branch Assistant',
    )
    RoleUserOrgAssociation.objects.get_or_create(
        user=branch_3_assistant_user,
        role=roles_obj_dict['Clinic-Assistant'],
        organization=branch_3,
    )




if __name__ == '__main__':
    with transaction.atomic():
        initialize_data()

        # raise Exception('All good!')
