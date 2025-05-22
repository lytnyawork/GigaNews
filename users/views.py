# views.py

from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from comment.models import Comment, User
from main.models import Article, Category
from reactions.models import ArticleReaction
from users.models import FavoriteArticle, Profile
from .forms import CustomPasswordChangeForm, LoginForm, RegisterForm, ProfileForm


def auth_view(request):
    active_tab = 'login'  # По умолчанию активна вкладка входа
    
    if request.method == 'POST':
        # Обработка формы входа
        if 'login-submit' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            register_form = RegisterForm()
            
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Вы успешно вошли в систему')
                    return redirect('home')  # Замените на нужный URL
            active_tab = 'login'
        
        # Обработка формы регистрации
        elif 'register-submit' in request.POST:
            register_form = RegisterForm(request.POST)
            login_form = LoginForm()
            
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрировались')
                return redirect('home')  # Замените на нужный URL
            active_tab = 'register'
    
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
    
    return render(request, 'users/auth_page.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': active_tab
    })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))




def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user_id=user.id)
    is_owner = request.user.id == user.id
    active_tab = request.GET.get('tab', 'favorites')

    if not is_owner and active_tab in ['profile', 'account']:
        raise Http404("Доступ запрещен")


    form = None
    password_form = None
    password_changed = False
    if is_owner and request.method == 'POST':
        if active_tab == 'profile':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('users:profile', user_id=user_id)
        
        elif active_tab == 'account':
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Пароль успешно изменен!')
                password_changed = True
                password_form = CustomPasswordChangeForm(user=request.user)


    favorites = FavoriteArticle.objects.filter(user_id=user_id)
    favorite_ids = favorites.values_list('article_id', flat=True)
    comments = Comment.objects.filter(author_id=user_id)
    reactions = ArticleReaction.objects.filter(user_id=user_id)
    favorite_articles = Article.objects.filter(id__in=favorite_ids)



    if is_owner:
        if active_tab == 'profile' and form is None:
            form = ProfileForm(instance=profile)
        elif active_tab == 'account' and password_form is None:
            password_form = CustomPasswordChangeForm(user=request.user)




    context = {
        'profile_user': user,
        'profile': profile,
        'form': form,
        'password_form': password_form,
        'is_owner': is_owner,
        'active_tab': active_tab,
        'favorite_articles': favorite_articles,
        'user_stats': {
            'favorites': favorites,
            'comments': comments,
            'reactions': reactions,
        }
    }
    
    return render(request, 'users/profile.html', context)







