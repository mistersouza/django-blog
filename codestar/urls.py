from django.contrib import admin
from django.urls import path
from blog import views as blog_views

urlpatterns = [
    path('blog/', blog_views.blog, name='blog'),
    path('admin/', admin.site.urls),
]
