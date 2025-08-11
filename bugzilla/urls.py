from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, CreateProjectView,ListProjectView, CreateBugView, ListBugView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('createproject/', CreateProjectView.as_view(), name='create_project'),
    path('listproject/', ListProjectView.as_view(), name='list_projects'),
    path('createbug/', CreateBugView.as_view(), name='create_bug'),
    path('listbugs/', ListBugView.as_view(), name='list_bugs'),

]