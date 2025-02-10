from django.urls import path
from dj_rest_auth.views import LogoutView
from .views import CustomLoginView, CustomUserDetailsView 

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user', CustomUserDetailsView.as_view(), name='user'),
]