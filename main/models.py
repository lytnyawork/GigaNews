from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import itertools
from django.db.models import Count
from reactions.models import ReactionType
from users.models import FavoriteArticle


# Create your models here.
class Article(models.Model):
    card_title = models.CharField(max_length=255, verbose_name="Заголовок карточки")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, verbose_name="URL-адрес"
    )
    rating = models.IntegerField(verbose_name="Рейтинг", default=0, db_index=True)
    card_text = models.TextField(verbose_name="Текст карточки")
    word_file = models.FileField(
        upload_to="articles/word_files/",
        verbose_name="Word-документ",
        help_text="Загрузите документ в формате .docx",
    )
    card_image = models.ImageField(
        upload_to="articles/images/",
        verbose_name="Изображение карточки",
        null=True,
        blank=True,
    )
    is_extra = models.BooleanField(default=False, verbose_name="Extra статья")
    time_create = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT)

    def update_rating(self):
        self.rating = (
            self.article_reactions.count() * 3
            + self.comments.count() * 5
            + self.favorites.count() * 7
        )
        self.save(update_fields=["rating"])

    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug пустой
            self.slug = self.generate_unique_slug(self.card_title)
        super().save(*args, **kwargs)

    def generate_unique_slug(self, title):
        """Генерация уникального slug на основе заголовка"""
        base_slug = slugify(title, allow_unicode=True)
        unique_slug = base_slug
        return unique_slug

    def __str__(self):
        return self.card_title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def get_reaction_counts(self):
        counts = self.article_reactions.values(  
            "reaction_type__code", "reaction_type__emoji"
        ).annotate(count=Count("id"))

        return {
            item["reaction_type__code"]: {
                "emoji": item["reaction_type__emoji"],
                "count": item["count"],
            }
            for item in counts
        }

    def get_user_reaction(self, user):
        if user.is_authenticated:
            reaction = self.article_reactions.filter(
                user=user
            ).first()  
            return reaction.reaction_type.code if reaction else None
        return None

    def is_favorite_by(self, user):
        """Проверяет, есть ли статья в избранном у пользователя"""
        if user.is_authenticated:
            return self.favorited_by.filter(user=user).exists()
        return False

    def toggle_favorite(self, user):
        if not user.is_authenticated:
            return False

        favorite, created = FavoriteArticle.objects.get_or_create(
            user=user, article=self
        )
        if not created:
            favorite.delete()
            return False
        return True


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cat", kwargs={"cat_slug": self.slug})
