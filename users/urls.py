

from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('auth/', views.auth_view, name='auth_page'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:user_id>', views.profile, name='profile'),
]
