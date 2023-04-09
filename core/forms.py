from django import forms 
from .models import Posts , CustomUser

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'description'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=False)

    class Meta:
        model = Posts
        fields = ['image', 'description', 'tags']


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['image', 'username', 'first_name', 'last_name', 'email', ]
        widgets = {
            'image' : forms.FileInput(attrs={"style": "width: 200px; height: 200px;"})
        }