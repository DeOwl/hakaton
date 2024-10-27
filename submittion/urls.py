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
from main_app.views import ratePrediction, user_ratePrediction, Login_User, logout_user, auth_ratePrediction, reg_ratePrediction
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ratePrediction, name='mainForm'),
    path('auth/', csrf_exempt(auth_ratePrediction), name='aForm'),
    path('login_user/', csrf_exempt(Login_User), name='lForm'),
    path('logout/', csrf_exempt(logout_user), name='logoutForm'),
    path('reg/', csrf_exempt(reg_ratePrediction), name='rForm'),
    path('weeks/<int:subject_id>', get_weeks, name='weeks'),
    path('user/<int:user_id>/post_subject/', csrf_exempt(post_subject), name='post_subject'),
    path('update_subject/', update_subject, name='update_subject'),
    path('delete_subject/', delete_subject, name='delete_subject'),
    path('post_week/<subject_id>', csrf_exempt(post_week), name='post_week'),
    path('user/<int:id>', get_subjects, name='uForm'),

]
