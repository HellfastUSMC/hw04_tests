from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('about/', include('about.urls', namespace='about')),
    path('', include('posts.urls', namespace='posts')),
]
