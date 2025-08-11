from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from bugzilla.models import Project, Bug

class Command(BaseCommand):
    help = 'Create user roles and assign permissions'
    def handle(self, *args, **kwargs):
        # Create roles
        manager_group, created = Group.objects.get_or_create(name='Manager')
        qa_group, created = Group.objects.get_or_create(name='QA')
        developer_group, created = Group.objects.get_or_create(name='Developer')

        create_permission = Permission.objects.get(codename='can_create_projects')
        assign_permission = Permission.objects.get(codename='can_assign_developers')
        report_permission = Permission.objects.get(codename='can_report_bugs')
        no_create_permission = Permission.objects.get(codename = 'cannot_create_projects')
        assign_bugs_permission = Permission.objects.get(codename='are_assigned_bugs')
        
        manager_group.permissions.add(create_permission, assign_permission)
        qa_group.permissions.add(report_permission)
        developer_group.permissions.add(no_create_permission, assign_bugs_permission)