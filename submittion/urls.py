"""
URL configuration for submittion project.

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
from django.urls import path
from main_app.views import ratePrediction, get_subjects, get_weeks, post_subject, update_subject, delete_subject, post_week
from main_app.views import ratePrediction, user_ratePrediction, auth_ratePrediction, reg_ratePrediction


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ratePrediction, name='mainForm'),
    path('auth/', auth_ratePrediction, name='aForm'),
    path('reg/', reg_ratePrediction, name='rForm'),
    path('weeks/', get_weeks, name='weeks'),
    path('post_subject/', post_subject, name='post_subject'),
    path('update_subject/', update_subject, name='update_subject'),
    path('delete_subject/', delete_subject, name='delete_subject'),
    path('post_week/', post_week, name='post_week'),
    path('userPrev/', user_ratePrediction, name='uForm'),
    path('user/<int:id>', get_subjects, name='userSubjects'),

]
