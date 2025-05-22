
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('cat/<slug:cat_slug>/', views.show_cat, name='cat'),
    path('toggle_favorite/<slug:post_slug>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)