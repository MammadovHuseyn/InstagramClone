from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to="User_Image" , default = '/User_Image/default-user.png')


    def __str__(self):
        return self.username

    def save(self , *args, **kwargs):
        self.username = self.username.lower()
        super(CustomUser , self).save(*args, **kwargs)
        if not Profile.objects.filter(user = CustomUser.objects.get(username=self.username)).exists():
            profile = Profile.objects.create(user = CustomUser.objects.get(username=self.username))
            profile.save()

        if Profile.objects.filter(user = CustomUser.objects.get(username=self.username)).exists():
            profile = Profile.objects.get(user = CustomUser.objects.get(username=self.username))
            profile.profiletag = '@' + self.username
            profile.save()
            
    class Meta:
        verbose_name_plural = 'Users'


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
    user = models.OneToOneField("CustomUser" , on_delete=models.CASCADE , related_name='profile')
    favorites = models.ManyToManyField(Posts , related_name = "post_favorites" , blank=True)
    profiletag = models.CharField(max_length=250 , null=True , blank= True)
    about = models.TextField(null=True , blank=True)

    def __str__(self):
        return self.user.username        

    def save(self , *args, **kwargs):
        self.profiletag = '@' + self.user.username
        super(Profile, self).save(*args, **kwargs)

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

    
class Story(Create):
    user = models.ForeignKey("CustomUser", on_delete = models.CASCADE , related_name= 'story')
    story_image = models.ImageField(upload_to='Story_Image')
    