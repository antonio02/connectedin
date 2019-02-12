from django import forms
from django.core.exceptions import ValidationError

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

    def clean(self):
        super().clean()
        if not self.cleaned_data['post_text'] and not self.cleaned_data['image']:
            raise ValidationError(_('Your post need a text or a image'), code='text_image_post_error')


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'].label = _('Comment')

    class Meta:
        model = Comment
        fields = [
            'comment_text',
        ]


class SharePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SharePostForm, self).__init__(*args, **kwargs)
        self.fields['post_text'].label = _('Diga algo')

    class Meta:
        model = Post
        fields = [
            'post_text',
        ]
