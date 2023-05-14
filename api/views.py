from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView , CreateAPIView , DestroyAPIView , RetrieveAPIView , UpdateAPIView

from .serializer import LikeSerializer , LikeListSerializer , CommentSerializer , FavoriteSerializer , FollowerSerializer
from core.models import Like , Posts , CustomUser , Favorite , Follower
from comment.models import Comment


class LikeAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

# class UnlikeAPIView(DestroyAPIView):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     lookup_field = "id"

class UnlikeAPIView(APIView):

    def delete(self, request , id):
        try:
            like = Like.objects.get(user = request.user , post = Posts.objects.get(id = id))
            post = Posts.objects.get(id = id)
            like.delete()
            post.likes -=1
            post.save()
            return Response(status= status.HTTP_200_OK)
           

        except Like.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND , data = {"message" : "Like not found"})

class LikeListAPIView(ListAPIView):
    
    serializer_class = LikeListSerializer
    lookup_field = "post_id"

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        likes = Like.objects.filter(post = Posts.objects.get(id = post_id))
        return likes
    

class CommentAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "post_id"

class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "post_id"

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post = Posts.objects.get(id = post_id))

class FavoriteAPIView(CreateAPIView):

    serializer_class = FavoriteSerializer
    lookup_field = "post_id"

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Favorite.objects.get(post = Posts.objects.get(id = post_id))

    
class UnFavoriteAPIView(APIView):

    def delete(self, request , post_id):
        try:
            fav = Favorite.objects.get(user = request.user , post = Posts.objects.get(id = post_id))
            fav.delete()
            return Response(status= status.HTTP_204_NO_CONTENT , data= {"message" : "Deleted successfully"})
           

        except Favorite.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND , data = {"message" : "Fav not found"})

    
class FollowerAPIView(CreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    lookup_field = "user_id"