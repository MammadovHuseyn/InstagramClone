from rest_framework.serializers import ModelSerializer , SerializerMethodField
from core.models import Like , Favorite , Follower 
from comment.models import Comment


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']

class LikeListSerializer(ModelSerializer):
    username = SerializerMethodField()
    class Meta:
        model = Like
        fields = ['username','user', 'post']

    def get_username(self , obj):
        return str(obj.user.username)

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post' , 'user' , 'body']

class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user' , 'post']

class FollowerSerializer(ModelSerializer):
    class Meta:
        model = Follower
        fields = ["follower" , "following"]
