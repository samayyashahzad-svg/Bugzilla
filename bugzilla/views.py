
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import CreateView, RedirectView, ListView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import SignUpForm, ProjectForm, BugForm
from django.contrib.auth.models import User
from .models import Project, Bug
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class SignUpView(CreateView):
    template_name = 'bugzilla/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class CustomLoginView(DjangoLoginView):
    template_name = 'bugzilla/login.html'

    def post(self, request):
        email = request.POST.get('email')  
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            usern = user_obj.username
            request.session['name'] = usern

        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)

            if user.groups.filter(name='Manager').exists():
                request.session['group'] = 'Manager'
                return redirect('list_projects')
            
            elif user.groups.filter(name='QA').exists():
                request.session['group'] = 'QA'
                return redirect('list_bugs')
            
            elif user.groups.filter(name='Developer').exists():
                request.session['group'] = 'Developer'
                return redirect('list_projects')
        else:
            return self.form_invalid(self.get_form())


class CustomLogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class CreateProjectView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'bugzilla/create_project.html'
    success_url = reverse_lazy('list_projects')
    permission_required = 'bugzilla.can_create_projects'

    def form_valid(self, form): 
        form.instance.manager = self.request.user
        response = super().form_valid(form)
        form.instance.developers.set(form.cleaned_data['developers'])
        return response


class ListProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'bugzilla/list_projects.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Project.objects.filter(manager=user)
        elif user.groups.filter(name='Developer').exists():
            return Project.objects.filter(developers=user)
        return Project.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('name')
        context['group'] = self.request.session.get('group')
        return context

class DetailProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'bugzilla/project_detail.html'
    context_object_name = 'project'

class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model = Project
    template_name = 'bugzilla/project_confirm_delete.html'
    success_url = reverse_lazy('list_projects')


class CreateBugView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Bug
    form_class = BugForm
    template_name = 'bugzilla/create_bug.html'
    success_url = reverse_lazy('list_bugs')
    permission_required = 'bugzilla.can_report_bugs'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ListBugView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'bugzilla/list_bugs.html'
    context_object_name = 'bugs'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='QA').exists():
            return Bug.objects.filter(creator=user)
        elif user.groups.filter(name='Developer').exists():
            return Bug.objects.filter(assigned_to=user)
        return Bug.objects.none()
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('name', 'Guest')
        context['group'] = self.request.session.get('group')
        return context    


class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = 'bugzilla/bug_detail.html'
    context_object_name = 'bug'

class BugUpdateView(LoginRequiredMixin,UpdateView):
    model = Bug
    fields = ['status']
    template_name = 'bugzilla/create_bug.html'
    success_url = reverse_lazy('list_bugs')

class BugDeleteView(LoginRequiredMixin,DeleteView):
    model = Bug
    template_name = 'bugzilla/bug_delete.html'
    success_url = reverse_lazy('list_bugs')
