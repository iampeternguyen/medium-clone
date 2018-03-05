from django.urls import path
from medium import views

app_name = 'medium'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]
