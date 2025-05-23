# Generated by Django 5.2 on 2025-05-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_title', models.CharField(max_length=255, verbose_name='Заголовок карточки')),
                ('card_text', models.TextField(verbose_name='Текст карточки')),
                ('word_file', models.FileField(help_text='Загрузите документ в формате .docx', upload_to='articles/word_files/', verbose_name='Word-документ')),
                ('card_image', models.ImageField(blank=True, null=True, upload_to='articles/images/', verbose_name='Изображение карточки')),
                ('is_extra', models.BooleanField(default=False, verbose_name='Extra статья')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
