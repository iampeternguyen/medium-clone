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
    path('unfollow/<author_pk>/<int:post_pk>',
         views.unfollow_user, name='unfollow_user'),
    path('follow/topic/<tag>', views.follow_topic, name='follow_topic'),
    path('unfollow/topic/<tag>', views.unfollow_topic, name='unfollow_topic'),

    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/cheer/', views.add_cheer, name='add_cheer'),
    path('post/<int:pk>/remove_cheer/', views.remove_cheer, name='remove_cheer'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),

    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('tags/<tag>', views.TagsListView.as_view(), name='tags'),

    path('post/<int:pk>/comment/delete',
         views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

    path('me/edit/', views.profile_edit, name='me_edit'),
    path('me/drafts/', views.DraftsListView.as_view(), name='drafts'),

    path('me/', views.my_profile, name='me'),

]
