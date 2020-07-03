from django.urls import path

from . import views

urlpatterns = [
    path('post/del-comm/<int:pk>/', views.delete_comment, name='delete-comment'),
]