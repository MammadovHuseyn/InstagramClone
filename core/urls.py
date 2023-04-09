from django.urls import path 
from .views import *
urlpatterns = [
    path('' , home , name='home'),
    path('detail/<int:id>/' , detail , name='detail'),
    path('like/<int:id>/' , like , name='like'),
    path('follow/' , follow , name = 'follow'),
    path('detail/<str:username>/' , user_detail , name = 'user_detail'), 
    path('favorites/<int:post_id>/' , favorites , name = 'favorites'),
    path('<str:username>/favorites/' , user_detail , name='favorite_posts'),
    path('newpost/' , newpost , name = 'newpost'),
    path('detail/<str:username>/followers/' , show_followers , name='show_followers'),
    path('detail/<str:username>/following/' , show_following , name='show_following'),
    path('detail/<int:id>/likes/' , show_likes , name='show_likes'),
    path('detail/<str:username>/editprofile/' , editprofile , name='editprofile'),
    
]
