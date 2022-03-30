import random
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView
from django.http import HttpResponse
from .models import News,Category,Comment
from .forms import NewsForm,UserRegisterForm,UserLoginForm,ContactForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from .models import Code
# Create your views here.

def user_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],form.cleaned_data['body'],'lubaskincorporation@gmail.com',['kanalpoznavatela1234@gmail.com'],fail_silently=True)
            if mail:
                messages.success(request,'Письмо отправлено')
                return redirect('home')
            else:
                messages.error(request,'Ошибка отправки! Возможно, сервер SMTP сейчас недоступен.')
        else:
            messages.error(request,'Ошибка заполнения письма!')
    else:
        form = ContactForm() # регистрация
    return render(request,'news/contact.html',context={'form':form})


def user_logout(request):
    logout(request)
    return redirect('auth')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            current_user = Code.objects.get(user_name=form.cleaned_data['username'])
            if form.cleaned_data['code'] == current_user.user_code:
                user = form.get_user()
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Неверный код!')
        else:
            messages.error(request,'Ошибка!')
    else:
        form = UserLoginForm()
    return render(request,'news/auth.html',context={'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Успешно! Мы отправили ваш персональный код на указанный email')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            random_code = random.randint(0,928710308)
            code = Code.objects.create(user_name=username,user_code=random_code)
            code.save()
            send_mail(f'Добро пожаловать, {username}',f'Благодарим за регистрацию,теперь вы можете авторизоваться.\nВам также доступна функция "Добавить новость", за глупые/лживые посты администрация вправе применить необходимые меры!\nВаш пароль: {password} , используйте его для входа\nВаш персональный код: {random_code} , используйте его для входа\nХорошего времени суток!','lubaskincorporation@gmail.com',[form.cleaned_data['email']])
            return redirect('auth')
        else:
            messages.error(request,'Ошибка!')
    else:
        form = UserRegisterForm() # регистрация
    return render(request,'news/reg.html',context={'form':form})

class HomeNews(ListView): # ListView
    model = News
    template_name = 'news/news_list.html' # путь к шаблону
    context_object_name = 'news'
    allow_empty = False # не показываем пустые категории
    paginate_by = 3 # пагинация
    #extra_context = {'title':'News-paper'} # подставляем переменные

    def get_context_data(self, *,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News-paper'
        return context
        #тот же код что снизу но меньше

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category') # фильтруем по чекбоксу # селект оптимизируем подробно смотри в доке

class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False # не показываем пустые категории
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(is_published=True,category_id=self.kwargs['category_id']).select_related('category')
    
    def get_context_data(self, *,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id']) # не много не понял но тут получаем в title текущую категорию
        return context

#class ViewNews(DetailView): # смотр каждой новости с новым классом
    #model = News
    #pk_url_kwarg = 'news_id'
    #template_name='news/view_news.html'

class CreateNews(LoginRequiredMixin,CreateView):# создаем класс add_news # делаем тлько для админа через миксин
    form_class = NewsForm # связываем классы
    template_name = 'news/add_news.html' 
    # и происходит автомат редирект на новость из за нашего метода get_absolute_url() джанго ище его по умолчанию
    # вот так вот просто!
    login_url = 'auth' # если не авторизован перебрасываем на рег

#def index(request): # обязательный аргумент
   # news = News.objects.all()
    #context = {
        #'news':news,
        #'title':'Список новостей',
    #}
    #return render(request,'news/index.html',context=context)

#def get_category(request,category_id):
    #context_object_name = 'news'
    #news = News.objects.filter(category_id=category_id,is_published=True)
    #category = Category.objects.get(pk=category_id)
    #context = {
        #'news':news,
        #'category':category,
    #}
    #return render(request,'news/category.html',context) # выборка новостей по категориям
def view_news(request,news_id):
        news_item = get_object_or_404(News,pk=news_id)
        comments = news_item.comments.filter(active=True)
        comment_form = CommentForm(data=request.POST or None)
        if request.user.is_authenticated:
            if request.method == 'POST':
                if comment_form.is_valid():
                    news_comment = comment_form.save(commit=False)
                    news_comment.news = news_item
                    news_comment.name = request.user
                    news_comment.save()
                    messages.success(request,'Ваш комментарий отправлен!')
                    return redirect('home')
                else:
                    messages.error(request,'Неправильно заполненный комментарий!')
            else:
                comment_form = CommentForm()
        return render(request,'news/view_news.html',context={'news_item':news_item,'comments':comments,'comment_form':comment_form})
    

#def add_news(request):
    #if request.method == 'POST':
       # form = NewsForm(request.POST)
        #if form.is_valid():
            #form_news = News.objects.create(**form.cleaned_data) # сохраняем данные из формы # ** распаковка словаря
            #news = form.save()
            #return redirect(news)
    #else:
        #form = NewsForm()
    #return render(request,'news/add_news.html',{'form':form})