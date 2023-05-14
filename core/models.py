from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to="User_Image" , default = '/User_Image/default-user.png')
    bio = models.TextField(null=True , blank=True)
    profiletag = models.CharField(max_length=250 , null=True , blank= True)

    def __str__(self):
        return self.username

    def save(self , *args, **kwargs):
        self.username = self.username.lower()
        self.profiletag = '@' + self.username
        super(CustomUser , self).save(*args, **kwargs)
        
            
    class Meta:
        verbose_name_plural = 'Users'

class Favorite(models.Model):
    user  = models.ForeignKey(CustomUser, on_delete = models.CASCADE , related_name="post_favorites")
    post  = models.ForeignKey("Posts",on_delete = models.CASCADE, related_name="post_favorites" , null=True , blank= True)

    def save(self , *args, **kwargs):
        if not Favorite.objects.filter(user=self.user , post=self.post).exists():
            super(Favorite, self).save(*args, **kwargs)

class Create(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Posts(Create):
    author = models.ForeignKey("CustomUser" , verbose_name  = 'author' ,on_delete= models.CASCADE)
    image = models.ImageField(upload_to='Post_Image')
    description = models.TextField(max_length=255)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tags", related_name='tags' , blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Posts'


class Profile(models.Model):
    pass
    # user = models.OneToOneField("CustomUser" , on_delete=models.CASCADE , related_name='profile')
    # image = models.ImageField(upload_to="User_Image" , default = '/User_Image/default-user.png')
   


    # bio = models.TextField(null=True , blank=True)

    # favorites = models.ManyToManyField(Posts , related_name = "post_favorites" , blank=True)
    # profiletag = models.CharField(max_length=250 , null=True , blank= True)

    # def __str__(self):
    #     return self.user.username        

    # def save(self , *args, **kwargs):
    #     self.profiletag = '@' + self.user.username

    #     self.username = self.user.username
    #     self.first_name = self.user.first_name
    #     self.last_name = self.user.last_name
    #     self.email = self.user.email
        
    #     super(Profile, self).save(*args, **kwargs)

class Tags(Create):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True , blank=True , unique= False , db_index= True , editable= True )
    
    def __str__(self):
        return self.name    

    def save(self , *args , **kwargs):
        self.slug = slugify(self.name)
        
        if Tags.objects.filter(slug = self.slug).exists():
            self.slug = self.slug + '-' + str(len(Tags.objects.filter(slug = self.slug)))

        if not self.name.startswith('#'):
            self.name = '#' + self.name

     
        if " " in self.name:
            self.name = self.name.replace(" ", "")
        

        super(Tags, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = ("Tags")


class Follower(models.Model):
    follower = models.ForeignKey("CustomUser" , on_delete=models.CASCADE , related_name='follower')
    following = models.ForeignKey("CustomUser" , on_delete=models.CASCADE , related_name='following')

    def __str__(self):
        return f"{self.follower} - {self.following}"
    
    def save(self , *args, **kwargs):
        if not Follower.objects.filter(follower=self.follower , following = self.following).exists() and self.follower != self.following:

            super(Follower, self).save(*args, **kwargs)          
            


class Like(Create):

    user = models.ForeignKey("CustomUser", on_delete = models.CASCADE , related_name= 'user_like')
    post = models.ForeignKey(Posts, on_delete = models.CASCADE , related_name= 'post_like')

    def __str__(self):
        return self.user.username

    def save(self , *args, **kwargs):

        if not Like.objects.filter(user = self.user , post = self.post):

            super(Like, self).save(*args, **kwargs)
            self.post.likes += 1
            self.post.save()
    
    def delete(self):

        self.post.likes -= 1
        super(Like, self).delete()

    
class Story(Create):
    user = models.ForeignKey("CustomUser", on_delete = models.CASCADE , related_name= 'story')
    story_image = models.ImageField(upload_to='Story_Image')
    