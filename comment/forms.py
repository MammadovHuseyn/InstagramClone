from django import forms
from .models import Comment 
class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input','style':'border:none; width:100%;outline:none;', 'placeholder': 'Write comment'}), required=True)
    
    class Meta:
        model = Comment
        fields = ("body",)