"""
URL configuration for hugo_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'cursos', views.CursoViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'secciones', views.SeccionViewSet)
router.register(r'bloques', views.BloqueViewSet)
router.register(r'requisitos', views.RequisitoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('reset-database/', views.clear_database, name='reset_database'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    #path('logout/', views.logout, name='logout'),
    path('get_horarios/', views.get_horarios, name='get_horarios'),
]
