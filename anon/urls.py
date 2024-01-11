from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('add-anonymous-message/<str:id>/', views.AddAnonymousMessage, name='add-anonymous-message'),
    path('all-anonymous-message/', views.AllAnonymousMessage, name='all-anonymous-message'),

    path('register', views.Register, name='register'),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
]
