from tokenize import Comment
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from users.models import FavoriteArticle

from .utils import get_category_of_the_day
from reactions.templatetags.reactions_tags import get_reaction_types
from main.models import Article, Category
from django.contrib.auth.decorators import login_required
from comment.forms import CommentForm, ReplyForm
from comment.models import Comment

import mammoth


def index(request):

    r_sort = Article.objects.order_by("-rating")

    extra_posts = Article.objects.filter(is_extra=True)

    last_three_extra = extra_posts[len(extra_posts) - 3 : len(extra_posts)]

    new_posts = Article.objects.order_by("-time_create")

    current_category = get_category_of_the_day()
    date_post = Article.objects.filter(cat=current_category)

    name_cat = Category.objects.get(id=current_category).name

    top_r = r_sort[0]

    r_bar = r_sort[1:5]

    cat = Category.objects.all()

    data = {
        "cat": cat,
        "top_r": top_r,
        "r_bar": r_bar,
        "extra_posts": last_three_extra[::-1],
        "new_posts": new_posts[:4],
        "name_cat": name_cat,
        "date_post": date_post[:4],
    }

    return render(request, "main/index.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug)

    document = post.word_file

    comments = post.comments.filter(parent__isnull=True)
    new_comment = None

    reply_form = ReplyForm()  
    if request.method == "POST":
        form_type = request.POST.get("form_type", "comment")

        if form_type == "parent":
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.article = post
                new_comment.author = request.user
                new_comment.save()
                return redirect(post.get_absolute_url() + f"#comment-{new_comment.id}")
        else:
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.article = post
                reply.author = request.user
                parent_id = request.POST.get("parent_id")
                if parent_id:
                    reply.parent = get_object_or_404(Comment, id=parent_id)
                reply.save()
                return redirect(post.get_absolute_url() + f"#comment-{reply.parent.id}")

    else:
        comment_form = CommentForm()

    # Конвертация документа
    with document.open("rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_content = result.value

    # Похожие статьи
    cat_post = Article.objects.filter(cat=post.cat).exclude(slug=post.slug)[:4][::-1]

    # Проверка избранного
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteArticle.objects.filter(
            user=request.user, article=post
        ).exists()

    data = {
        "is_favorite": is_favorite,
        "post": post,
        "content": html_content,
        "reaction_types": get_reaction_types(),
        "reaction_counts": post.get_reaction_counts(),
        "cat_post": cat_post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": CommentForm(),
        "reply_form": ReplyForm(),
        "user_reaction": (
            post.get_user_reaction(request.user)
            if request.user.is_authenticated
            else None
        ),
    }

    return render(request, "main/post.html", data)


@login_required
def toggle_favorite(request, post_slug):
    post = get_object_or_404(Article, slug=post_slug)

    favorite, created = FavoriteArticle.objects.get_or_create(
        user=request.user, article=post
    )

    if not created:
        favorite.delete()

    return redirect("post", post_slug=post_slug)


def show_cat(request, cat_slug):
    cat = Category.objects.get(slug=cat_slug)
    cat_id = cat.id
    posts = Article.objects.filter(cat=cat_id)
    cat_all = Category.objects.all()

    data = {"cat": cat_all, "posts": posts}

    return render(request, "main/cat.html", data)


def search(request):

    query = request.GET.get("q", "")
    category_filter = request.GET.get("category", "all")
    sort_by = request.GET.get("sort", "relevance")

    articles = Article.objects.all()

    if query:
        articles = articles.filter(
            Q(card_title__icontains=query) | Q(card_text__icontains=query)
        )

    if category_filter != "all":
        articles = articles.filter(cat__slug=category_filter)

    if sort_by == "date":
        articles = articles.order_by("time_create")
    else:
        articles = articles.order_by("-rating")

    categories = Category.objects.all()

    context = {
        "query": query,
        "articles": articles,
        "categories": categories,
        "selected_category": category_filter,
        "sort_by": sort_by,
        "results_count": articles.count(),
    }

    return render(request, "main/search.html", context)
