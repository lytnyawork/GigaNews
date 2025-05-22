from django.contrib import admin
from .models import Article, Category
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('card_title', 'slug')
    prepopulated_fields = {'slug': ('card_title',)}  # Автозаполнение slug при вводе title

admin.site.register(Category)
