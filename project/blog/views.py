from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Article, Comment, Profile, Mark
from .forms import ArticleForm, LoginFrom, RegistrationForm, CommentForm, ProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages
from random import randint


class ArticleList(ListView):
    model = Article
    template_name = 'blog/index.html'
    extra_context = {'title': 'ERIELL NEWS'}
    context_object_name = 'articles'


class CategoryList(ArticleList):
    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Category: {category.title}'
        return context


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()

        user = self.request.user
        if user.is_authenticated:
            mark, created = Mark.objects.get_or_create(user=user, article=article)
            context['like'] = mark.like
            context['dislike'] = mark.dislike
        else:
            context['like'] = False
            context['dislike'] = False

        likes_count = Mark.objects.filter(article=article, like=True).count()
        dislikes_count = Mark.objects.filter(article=article, dislike=True).count()
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count



        context['title'] = f'Article: {article.title}'
        context['comments'] = article.comments.filter(parent=None)
        articles = Article.objects.all()
        articles = articles.order_by('views')
        context['articles'] = articles[:3]
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context


class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('article', article.pk)

    else:
        form = ArticleForm()

    context = {
        'title': "Add new Article",
        'form': form
    }
    return render(request, 'blog/add_article.html', context)


class AddArticle(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add_article.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add_article.html'
    extra_context = {'title': 'article edit'}


def user_login(request):
    if request.method == 'POST':
        form = LoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Success login')
            return redirect('index')
        else:
            messages.error(request, 'Error login/password')
            return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request, 'Registration complete')
            return redirect('index')
        else:
            messages.error(request, 'Register ERROR. Try again')
            return redirect('index')


def user_logout(request):
    logout(request)
    return redirect('index')


def save_comment(request, pk):
    if request.method == 'POST':
        parent_pk = request.POST.get('parent', None)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = Article.objects.get(pk=pk)
            comment.user = request.user
            comment.parent = Comment.objects.get(pk=parent_pk)
            comment.save()
            return redirect('article', pk)


def random_article_view(request):
    articles = Article.objects.all()
    len_articles = len(articles)
    random_index = randint(0, len_articles - 1)
    article = articles[random_index]
    return redirect('article', article.pk)


class SearchResults(ArticleList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(title__icontains=word)
        return articles


def profile_view(request, pk):
    if request.method == 'POST':
        profile = Profile.objects.get(user_id=pk)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk)
    else:
        profile = Profile.objects.get(user_id=pk)
        count_articles = Article.objects.filter(user_id=pk).count()
        count_comments = Comment.objects.filter(user_id=pk).count()
        count_likes = 0
        articles = Article.objects.filter(user_id=pk)
        for article in articles:
            likes = Mark.objects.filter(article=article, like=True).count()
            count_likes += likes
        context = {
            'profile': profile,
            'title': 'My profile',
            'count_articles': count_articles,
            'count_comments': count_comments,
            'count_likes': count_likes
        }
        form = ProfileForm(instance=profile)
        context['form'] = form
        return render(request, 'blog/profile.html', context)


def add_or_delete_mark(request, article_id, action):
    # add_like, add_dislike, delete_like, delete_dislike
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Mark.objects.get_or_create(user=user, article=article)
        if action == 'add_like':
            mark.like = True
            mark.dislike = False
        elif action == 'add_dislike':
            mark.like = False
            mark.dislike = True
        elif action == 'delete_like':
            mark.like = False
        elif action == 'delete_dislike':
            mark.dislike = False
        mark.save()
        return redirect('article', article_id)
    else:
        return redirect('article', article_id)
