from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.hashers import check_password

from core.models import Posts , Create , Profile , Tags  , Follower , Like , CustomUser , Favorite 
from comment.models import Comment
from .forms import PostForm , UserUpdateForm , ChangePasswordForm
from comment.forms import CommentForm

# Create your views here.



@login_required(login_url='login')
def home(request):
   
    #Show posts shared by users I follow on my homepage
    
    #Users I follow 
    follower = Follower.objects.filter(follower = request.user )
    #Their posts
    posts = Posts.objects.filter(Q(author__following__in = follower) | Q(author = request.user)).order_by("-created")
    # posts.append(Posts.objects.filter(author = request.user))

    #Suggestions for users I follow 
    #Users I followed
    s = list(Follower.objects.filter(follower = request.user))
    my_following = [f.following for f in s if f.following != request.user ]
    
    #These users follow
    following_users = Follower.objects.filter(follower__in = my_following )
    userlist = []
    for f in following_users:
        
        if f.following not in userlist and f.following not in my_following and f.following != request.user:
            userlist.append(f.following)


   
    #Liked and favorite posts
    liked_posts =[l.post for l in Like.objects.filter(user=request.user).all()]
    favorites_posts = [Posts.objects.get(id = l.post.id) for l in Favorite.objects.filter(user=request.user)]

    context = {
        'posts': posts,
        'recommed_users' : userlist,
        'my_following' : my_following , 
        'liked_posts' : liked_posts ,
        'favorites_posts' : favorites_posts ,
    }    

    #Search for users and post tags

    search_input = request.GET.get('search')
    if search_input:
        if search_input.startswith('@') and len(search_input)>1:  

            u = CustomUser.objects.filter(profiletag__icontains=search_input)
            users = [user for user in u]
            context['users'] = users

            return render(request, 'core/profilesearch.html', context)

        elif search_input.startswith('#'):
            
            posts = Posts.objects.filter(tags__name = search_input)
            context['posts'] = posts
            context['search_text'] = search_input

            return render(request, 'core/tagsearch.html' , context)

    #Comment
    context['form'] = CommentForm()
    
    return render(request , 'core/index.html' , context)

@login_required(login_url='login')
def follow(request):

    if request.method == 'POST':

        value = request.POST['value']
        follower = CustomUser.objects.get(username= request.POST['follower'])        
        following = CustomUser.objects.get(username = request.POST['following'])
        if value == 'p_follow':
            flw = Follower.objects.create(follower = follower , following= following)
            flw.save()             
            return redirect('user_detail' , username = following)

        elif value == 'p_unfollow':
            flw = Follower.objects.get(follower = follower , following= following)
            flw.delete()          
            return redirect('user_detail' , username = following)

        elif value == 'search_follow':
            flw = Follower.objects.create(follower = follower , following= following)
            flw.save()             
           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif value == 'search_unfollow':
            flw = Follower.objects.get(follower = follower , following= following)
            flw.delete()     
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        elif value == 'remove_follower':            
            flw = Follower.objects.get(follower = follower , following= following)
            flw.delete()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if value == 'follow':
            flw = Follower.objects.create(follower = follower , following= following)
            flw.save()
            return redirect('home')

    return redirect(home)
        

@login_required(login_url='login')
def detail(request , id):
    post = get_object_or_404(Posts , id = id)
    comments = Comment.objects.filter(post = post)
    liked_posts =[l.post for l in Like.objects.filter(user=request.user).all()]
    favorites_posts = [Posts.objects.get(id = l.post.id) for l in Favorite.objects.filter(user=request.user)]
    
    #comments 
    if request.method == 'POST':
        if request.POST.get('value') == 'delete_comment':
            
            comment =Comment.objects.filter(id = request.POST['comment'])
            comment.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'post' : post,
        'liked_posts' : liked_posts,
        'comments' : comments,
        'form' : CommentForm(),
        'favorites_posts' : favorites_posts,
    }

    return render(request , 'core/details.html', context )


@login_required(login_url='login')
def like(request , id):

    if request.method == 'POST':
        if request.POST.get('value') == 'detail_post':
            user = request.user
            post = Posts.objects.get(id=id)
            current_like = post.likes
            
            liked = Like.objects.filter(user=user , post=post).count()

            if not liked:
                Like.objects.create(user=user , post=post)
                current_like += 1
            else:
                Like.objects.filter(user=user, post=post).delete()
                current_like -= 1
            post.likes = current_like
            post.save()

            
            return redirect('detail' , id = post.id)
        else:
      
            user = request.user
            post = Posts.objects.get(id=id)
      
            current_like = post.likes
       
            liked = Like.objects.filter(user=user , post=post).count()
        

            if not liked:
                Like.objects.create(user=user , post = post)
                current_like += 1
            
            else:
                Like.objects.filter(user=user, post=post).delete()
                current_like -= 1
              
            post.likes = current_like
            post.save()


            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def user_detail(request , username):
    user = CustomUser.objects.get(username=username)
    user_follower = Follower.objects.filter(following = user).all()
    user_following = Follower.objects.filter(follower = user).all()
    user_posts = Posts.objects.filter(author=user).all().order_by('-created')
    user_posts_count = user_posts.count()    
    
    if Follower.objects.filter(follower = request.user , following= user).exists():
        followcheck = True
    else:
        followcheck = False

   
    context = {
        "user":user,
        "user_following":user_following,
        "user_follower" : user_follower,
        "user_posts":user_posts,
        "user_posts_count":user_posts_count,
        'followcheck':followcheck,
    }

    if request.method == 'POST':
        if request.POST['action'] == 'favorited':
            user = CustomUser.objects.get(username = username)
            fav = [f for f in Favorite.objects.filter(user = user)]
            
            if len(fav) == 0:
                context['msg'] = "You haven't saved anything..."
            context['user_posts'] = fav
            context['page'] = "favorited"
            
        elif request.POST['action'] == 'allposts':
            context['user_posts'] = user_posts

    return render(request, 'core/profile.html' , context)

@login_required(login_url='login')
def editprofile(request , username ):

   
    user = get_object_or_404(CustomUser , username=username)
    form = UserUpdateForm(request.POST or None , files=request.FILES or None , instance= user)
    password_form = ChangePasswordForm(request.POST or None)
    error = None
    
    if request.method == "POST":

        if request.POST.get("value") == "edit_profile":
            profile_form = UserUpdateForm(request.POST or None , files=request.FILES or None)
            if profile_form.is_valid():
                profile_form.save()
                return redirect("editprofile")

        elif request.POST.get("value") == "change_password":
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                repassword = password_form.cleaned_data["repassword"]
                password = password_form.cleaned_data["password"]
                old_password = password_form.cleaned_data["old_password"]
                if password == repassword:
                    if check_password(old_password,user.password ):
                        user.set_password(password)
                        user.save()
                        return redirect("login")
                    else:
                        context['error'] = "Old password do not match"
                else:
                    context["error"] = "Passwords do not match" 

            
    # if request.POST['value'] == "edit_profile":
    #     print(form)

    # if request.POST.get('value') == 'change_password':
        
    #     if form.is_valid():
    #         repassword = form.cleaned_data["repassword"]
    #         password = form.cleaned_data["password"]
    #         old_password = form.cleaned_data["old_password"]
    #         current_password = request.user.password
    #         print(request.POST)
    #         if check_password(current_password, old_password):
    #             print('eyni')
            
    #         print(old_password)
    #         print(request.user.password)
    #         if request.user.password == old_password:
    #             print(True)
        
    # if form.is_valid():       
       
    
    #     form.save()
    #     return redirect("user_detail" , username = user.username)

        # else:
        #     error = "Passwords do not match"

    context={
        "form" : form,
        "password_form" : password_form,
        'error' : error
    }
    
   
    
    return render(request, 'core/editprofile.html' , context)

@login_required(login_url='login')
def favorites(request , post_id):
    user = request.user
    post = Posts.objects.get(id=post_id)
    profile = CustomUser.objects.get(username = user)
    print(profile.favorites.all())
    if request.POST.get('value') == 'favorited':
        if profile.favorites.filter(id = post.id).exists():
            profile.favorites.remove(post)
        else:
            profile.favorites.add(post)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def newpost(request):
    tag_list = []
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES )
        if form.is_valid():
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            tags = list(form.cleaned_data['tags'].split(','))
            
            post = Posts.objects.create(author= request.user , image = image , description= description)
           
            for tag in tags:
                if Tags.objects.filter(name = '#' + tag).exists():
                    t = Tags.objects.get(name = '#'+ tag)
                else:
                    t = Tags.objects.create(name = tag)

                tag_list.append(t)

            post.tags.set(tag_list)

            
            
         
            post.save()
            
            return redirect('home')
    context = {
        'form': PostForm()
    }
    
    return render(request, 'core/sharepost.html' , context)


def show_followers(request , username ):

    user = get_object_or_404(CustomUser , username = username)
    followers = [CustomUser.objects.get(username = f.follower) for f in user.following.all() if f != request.user]
    following = [CustomUser.objects.get(username = f.following) for f in user.follower.all() if f != request.user]

    my_following = [CustomUser.objects.get(username = user.following) for user in Follower.objects.filter(follower = request.user)]
    context = {
        "followers" : followers,
        "following" : following,
        'user' : CustomUser.objects.get(username = username),
        'my_following' : my_following,
    }
    return render(request, 'core/followers.html' , context )

def show_following(request , username):

    user = get_object_or_404(CustomUser , username = username)
    followers = [CustomUser.objects.get(username = f.follower) for f in user.following.all() if f != request.user]
    following = [CustomUser.objects.get(username = f.following) for f in user.follower.all() if f != request.user]

    my_following = [CustomUser.objects.get(username = user.following) for user in Follower.objects.filter(follower = request.user)]
    context = {
        "followers" : followers,
        "following" : following,
        'user' : CustomUser.objects.get(username = username),
        'my_following' : my_following,
    }
    return render(request, 'core/following.html' , context )

def show_likes(request, id):

    post = get_object_or_404(Posts , id=id)
    likes =[CustomUser.objects.get(username = like.user) for like in post.post_like.all() ] 
    my_following = [CustomUser.objects.get(username = user.following) for user in Follower.objects.filter(follower = request.user)]

    context = {
        "likes" : likes,
        "my_following" : my_following,
    }

    return render(request, 'core/likes.html', context)