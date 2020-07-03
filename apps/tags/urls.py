from django.urls import path

from . import views


urlpatterns = [
    path('', views.tags_list, name='tag-list'),
    path('create/', views.tag_create, name='tag-create'),
    path('<int:pk>/', views.tag_detail, name='tag-detail')
]