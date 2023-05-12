import os

from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from dotenv import load_dotenv


class PostsList(ListView):
    paginate_by = 3
    model = Post
    ordering = 'time'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(PostsList, self).get_context_data(**kwargs)
        return context


class SearchAuthor(ListView):
    model = Author
    context_object_name = 'author'


class SearchPosts(ListView):
    paginate_by = 3
    model = Post
    ordering = 'time'
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_filter'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        context['is_not_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        context['is_not_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить статью"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить новость"
        context['is_not_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать новость"
        context['is_not_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Удалить новость"
        context['previous_page_url'] = reverse_lazy('posts_list')
        return context
    
    
class AddProduct(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal_app.view_post',
                           'news_portal_app.add_post',
                           'news_portal_app.change_post',
                           )


class CategorySubscribeView(ListView):
    model = Category
    template_name = 'post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super(CategorySubscribeView, self).get_context_data(**kwargs)
        return context


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    category.subscribers.add(user)
    email = user.email
    send_mail(
        subject=f'News Portal: подпишись на обновления категории {category}',
        message=f'"{email}", вы подписались на обновления категории {category}',
        from_email='exampleforSF@yandex.ru',
        recipient_list=[f'{email}', ],
    )
    return redirect('/news')