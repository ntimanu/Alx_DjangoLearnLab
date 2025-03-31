from django import forms
from .models import Comment, Post, Tag

class TagWidget(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'tag-input', 'placeholder': 'Enter tags, separated by commas'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        if value and isinstance(value, (list, tuple)):
            tags = Tag.objects.filter(id__in=value)
            return ', '.join(tag.name for tag in tags)
        return super().format_value(value)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'})

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=TagWidget(),
        help_text="Enter tags separated by commas"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter post title'})
        self.fields['content'].widget = forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 10, 
            'placeholder': 'Write your post content here...'
        })
        
        if self.instance and self.instance.pk:
            self.initial['tags'] = ','.join(tag.name for tag in self.instance.tags.all())
    
    def clean_tags(self):
        tag_names = self.cleaned_data.get('tags', '')
        if not tag_names:
            return []
            
        tag_names = [name.strip() for name in tag_names.split(',') if name.strip()]
        return tag_names
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            tag_names = self.cleaned_data.get('tags', [])
            post.tags.clear()
            
        
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                post.tags.add(tag)
                
        return post
