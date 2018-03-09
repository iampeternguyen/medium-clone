from django.urls import path
from medium import views

app_name = 'medium'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new/', views.NewPostView.as_view(), name='new'),
    path('new2/', views.new_post, name='new2'),
    path('follow/<author_pk>/<int:post_pk>',
         views.follow_user, name='follow_user'),
    path('follow/topic/<pk>', views.follow_topic, name='follow_topic'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('search/', views.search_posts, name='search'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tags/<pk>', views.TagsListView.as_view(), name='tags'),

    path('post/<int:pk>/comment/delete',
         views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

    path('me/edit/', views.profile_edit, name='profile_edit'),
]
