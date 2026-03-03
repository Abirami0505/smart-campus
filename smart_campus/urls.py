from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Main Pages
    path('', views.dashboard, name='dashboard'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('qr/<int:reg_id>/', views.my_qr, name='my_qr'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('unregister-event/<int:event_id>/', views.unregister_event, name='unregister_event'),
    path('mark-attendance/<int:reg_id>/', views.mark_attendance, name='mark_attendance'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)