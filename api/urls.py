from django.urls import path 
from .views import LikeAPIView , UnlikeAPIView , LikeListAPIView , CommentAPIView , CommentListAPIView , FavoriteAPIView , UnFavoriteAPIView , FollowerAPIView

urlpatterns = [
    path('like/<int:id>/' , LikeAPIView.as_view() , name = "like_api"),
    path('unlike/<int:id>/' , UnlikeAPIView.as_view() , name = "unlike_api"),
    path('likes/<int:post_id>/' , LikeListAPIView.as_view() , name = "likes_api"),

    path('comment/<int:post_id>/' , CommentAPIView.as_view() , name="comment_api"),
    path('comment/list/<int:post_id>/' , CommentListAPIView.as_view() , name="comment_list_api"),

    path('fav/<int:post_id>/' , FavoriteAPIView.as_view() , name = "fav_api"),
    path('unfav/<int:post_id>/' , UnFavoriteAPIView.as_view() , name = "unfav_api"),

    path('follow/<int:user_id>/' , FollowerAPIView.as_view() , name = "follow_api"),

]
