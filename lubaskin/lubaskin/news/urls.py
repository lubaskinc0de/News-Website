from django.urls import path
from .views import HomeNews,NewsByCategory,CreateNews,register,user_login,user_logout,user_contact_form,view_news

urlpatterns = [
    #path('',index,name='home'),
    path('',HomeNews.as_view(),name='home'), # через ListView # кэшируем страницу на 60 сек
    path(f'category/<int:category_id>/',NewsByCategory.as_view(),name='category'), # просмотр разных категорий
    #path('news/<int:news_id>/',ViewNews.as_view(),name='view_news'), # просмотр полной новости
    path('news/<int:news_id>/',view_news,name='view_news'), # просмотр полной новости
    path('news/add-news',CreateNews.as_view(),name='add_news'),
    path('register/',register,name='reg'),
    path('auth/',user_login,name='auth'),
    path('logout/',user_logout,name='logout'),
    path('help/',user_contact_form,name='contact'),
]