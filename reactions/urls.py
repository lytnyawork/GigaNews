from django.urls import path
from . import views
from main import views as v



urlpatterns = [
    path('post/', views.handle_reaction, name='handle_reaction'),
        
]