from django.contrib import admin
from bugzilla.models import User, Project, Bug
# Register your models here.

admin.site.register(Project)
admin.site.register(Bug)