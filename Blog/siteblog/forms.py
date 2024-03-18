from django import forms
from django.forms import TextInput, Textarea

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Имя отправителя",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_from = forms.EmailField(label="Почта отправителя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_to = forms.EmailField(label="Почта получателя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}),
                               label="Комментарии")


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'body': 'Текст'
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=128, label="Поиск", widget=forms.TextInput(attrs={'class': 'form-control me-2',
                                                                                         'type': 'search',
                                                                                         'placeholder': 'Поиск',
                                                                                         'aria-label': "Поиск"}))
