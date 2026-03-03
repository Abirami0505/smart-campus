from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Student
    path('', views.dashboard, name='dashboard'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('qr/<int:reg_id>/', views.my_qr, name='my_qr'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]