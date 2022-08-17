from django.urls import path
from user.views import LoginView, LogoutView, DashboardView, RegisterView

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
]