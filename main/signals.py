from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from comment.models import Comment
from reactions.models import ArticleReaction
from users.models import FavoriteArticle


@receiver([post_save, post_delete], sender=ArticleReaction)
def update_rating_on_reaction(sender, instance, **kwargs):
    instance.article.update_rating()

@receiver([post_save, post_delete], sender=Comment)
def update_rating_on_comment(sender, instance, **kwargs):
    instance.article.update_rating()


@receiver([post_save, post_delete], sender=FavoriteArticle)
def update_rating_on_favorite(sender, instance, **kwargs):
    instance.article.update_rating()