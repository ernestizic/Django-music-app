from django import forms
from .models import Song, SongComment


class SongCommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please login to drop a comment',
                'rows': '4',
                'cols': '50'
            }
        )
    )

    class Meta:
        model = SongComment
        fields = ('content',)
