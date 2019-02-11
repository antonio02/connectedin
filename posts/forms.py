from django import forms
from .models import Post
from django.utils.translation import ugettext_lazy as _

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['post_text'].label    = _('New Post')

    class Meta:
        model = Post
        fields = [
            'post_text', 'image'
        ]