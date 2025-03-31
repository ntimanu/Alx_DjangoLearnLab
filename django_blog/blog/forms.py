from django import forms
from .models import Comment, Post, Tag

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'})

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
