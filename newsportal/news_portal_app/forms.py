from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    required_css_class = 'my-custom-class'
    title = forms.CharField(max_length=40)

    class Meta:
        model = Post
        fields = ['title', 'author', 'type', 'category', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})
        self.fields['title'].label = "Название статьи"
        self.fields['title'].widget.attrs.update({'placeholder': "Введите название"})
        self.fields['author'].label = "Автор"
        self.fields['author'].widget.attrs.update({'placeholder': "Имя автора"})
        self.fields['text'].label = "Текст статьи"
        self.fields['text'].widget.attrs.update({'placeholder': "Введите текст здесь"})
        self.fields['category'].label = "Категория статьи"
        self.fields['category'].widget.attrs.update({'placeholder': "Введите категорию статьи"})

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст статьи не должен быть идентичен заголовку."
            )
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user