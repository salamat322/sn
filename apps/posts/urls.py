from django.urls import path

from . import views
from apps.comments.views import delete_comment

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('<int:pk>/', views.post_detail, name='post-detail'),
    path('create/', views.create_post, name='post-create'),
    #path('<int:pk>/delete/', views.delete_post, name='post_delete'),
    path('<int:pk>/update/', views.update_post, name='post_update'),
    path('post/del-comm/<int:pk>/', delete_comment, name='delete-comment'),
]