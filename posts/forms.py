from django import forms
from .models import Post, Comment
from django.utils.translation import ugettext_lazy as _


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_text'].label = _('New Post')

    class Meta:
        model = Post
        fields = [
            'post_text', 'image'
        ]


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'].label = _('Comment')

    class Meta:
        model = Comment
        fields = [
            'comment_text',
        ]
