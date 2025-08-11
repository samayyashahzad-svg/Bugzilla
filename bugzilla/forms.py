# forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Bug

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ChoiceField(
        choices=[('Manager', 'Manager'), ('QA', 'QA'), ('Developer', 'Developer')],
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            group_name = self.cleaned_data['group']
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
        return user


class ProjectForm(forms.ModelForm):
    developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name='Developer'),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'developers']


class BugForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Developer'),
        required=True
    )
    bug_type = forms.ChoiceField(
        choices=Bug.BUG_TYPE_CHOICES,
        required=True  
    )

    class Meta:
        model = Bug
        fields = ['title', 'description', 'bug_type', 'status', 'image', 'project', 'assigned_to']
