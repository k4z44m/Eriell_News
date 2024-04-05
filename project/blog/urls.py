from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>', category_page, name='category'),
    # path('article/<int:pk>', article_detail, name='article'),
    # path('add_article/', add_article, name='add_article'),
    path('', ArticleList.as_view(), name='index'),
    path('category/<int:pk>', CategoryList.as_view(), name='category'),
    path('article/<int:pk>', ArticleDetail.as_view(), name='article'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='delete'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('random', random_article_view, name='random'),
    path('search/', SearchResults.as_view(), name='search'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('mark/<int:article_id>/<str:action>', add_or_delete_mark, name='mark')
]

