from django.urls import path
from .views import UserView,CustomLoginView 
from django.contrib.auth.views import LogoutView
app_name = 'users'

urlpatterns = [
    path('test', UserView.as_view(), name='user-home'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
]
