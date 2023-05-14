from django import forms 
from .models import Posts , CustomUser

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'description'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=False)

    class Meta:
        model = Posts
        fields = ['image', 'description', 'tags']


class UserUpdateForm(forms.ModelForm):

    image = forms.ImageField(widget=forms.FileInput(attrs= {"style": "width:145px; margin-left:25px;"}),required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'username',"style": "margin-right:10px;margin-bottom:10px;"}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First name',"style": "margin-right:10px;margin-bottom:10px"}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last name'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'email'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'bio' , "style":"width:375px;height:100px;outline:none;resize:none;border-style;groove;",}), required=False)
   

    class Meta:
        model = CustomUser
        fields = ('image', 'username', 'first_name', 'last_name', 'email', 'bio' )
            
class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'New Password',"style": "margin-right:10px;margin-bottom:10px;"}), required=False)
    repassword  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Repeat Password',"style": "margin-right:10px;margin-bottom:10px;"}), required=False)
    old_password  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter Your Old Password',"style": "margin-right:10px;margin-bottom:10px;"}), required=False)
        