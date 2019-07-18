from django.contrib import admin
from django.urls import path

from WebGraph import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('login/', views.validate_login),
    path('main/', views.index),
    path('analyze_data/', views.analyze_data),
    path('result/', views.result),
    path('logout/', views.logout_system),
]
