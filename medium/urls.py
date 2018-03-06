from django.urls import path
from medium import views

app_name = 'medium'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new/', views.NewPostView.as_view(), name='new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('search/', views.search_posts, name='search'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),



]
