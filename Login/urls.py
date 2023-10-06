from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.redirect_login, name='redirect_login'),
    path('logout/', views.logout_view, name='logout'),
]
