from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, CreateProjectView,ListProjectView, CreateBugView, ListBugView, DetailProjectView, ProjectDeleteView, BugDetailView, BugDeleteView, BugUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('createproject/', CreateProjectView.as_view(), name='create_project'), #M
    path('listproject/', ListProjectView.as_view(), name='list_projects'),      #M, #D

    path('createbug/', CreateBugView.as_view(), name='create_bug'),     #Q
    path('listbugs/', ListBugView.as_view(), name='list_bugs'),         #Q, D
    
    path('projectdetail/<int:pk>/', DetailProjectView.as_view(), name='project_detail'),
    path('projectdetail/<int:pk>/delete', ProjectDeleteView.as_view(), name='project_delete'),
    path('bugdetail/<int:pk>/', BugDetailView.as_view(), name='bug_detail'),
    path('bugedit/<int:pk>/edit', BugUpdateView.as_view(), name='bug_edit' ),
    path('bugdetail/<int:pk>/delete', BugDeleteView.as_view(), name='bug_delete'),
]