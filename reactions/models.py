from django.db import models
from django.conf import settings



class ReactionType(models.Model):
    """Типы реакций"""
    name = models.CharField(max_length=50, unique=True)
    emoji = models.CharField(max_length=5)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"




class ArticleReaction(models.Model):
    article = models.ForeignKey(
        'main.Article',
        on_delete=models.CASCADE,
        related_name='article_reactions'  # Изменяем related_name
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.ForeignKey('ReactionType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')
        verbose_name = 'Article Reaction'
        verbose_name_plural = 'Article Reactions'