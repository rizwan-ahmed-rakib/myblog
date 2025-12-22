from django import forms
from my_blog.models import Blog, Blog_comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Blog_comment
        fields = ('comment',)
