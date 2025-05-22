from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from main.models import Article
from reactions.models import ArticleReaction, ReactionType

@require_POST
@login_required
def handle_reaction(request):
    try:
        article_id = request.POST['article_id']  # Явное получение без get()
        reaction_type_id = request.POST['reaction_type_id']
        
        article = get_object_or_404(Article, id=article_id)
        reaction_type = get_object_or_404(ReactionType, id=reaction_type_id)
        
        # Используем update_or_create для атомарности
        ArticleReaction.objects.update_or_create(
            article=article,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        print(f"Статья: {article.id}, Реакция: {reaction_type.id}, Пользователь: {request.user.id}")
        
        return redirect('post', post_slug=article.slug)
    
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки реакции: {e}")  # Логируем в консоль
        return redirect('home')