from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from blog.models import Post, Comment
from .forms import CommentForm, ArticleCreatorForm
from jsonschema import ValidationError, validate
from blog.schemas import ARTICLE_SCHEMA


class CreateArticle(View):
    def get(self, request, user_id):
        if request.user.is_authenticated and request.user.id == int(user_id):
            form = ArticleCreatorForm()
            context = {
                "form": form,
                "user": user_id,
            }
            return render(request, "article_creator.html", context=context)
        else:
            return HttpResponse(status=401)

    def post(self, request, user_id):
        try:
            user_name = User.objects.get(id=user_id)
            validate(dict(request.POST), ARTICLE_SCHEMA)
            body_article = request.POST['body']
            title_article = request.POST['title']
            article = Post(user=user_name, title=title_article, body=body_article)
            article.save()
            return redirect("article_index", user_id)
        except ValidationError as exc:
            return JsonResponse({'error': exc.message}, status=401)


def article_index(request, user):
    try:
        user = User.objects.get(id=user)
        posts = Post.objects.filter(user=user).order_by('-created_on')
        context = {
            "posts": posts,
            "user_id": user.id,
        }
    except:
        return HttpResponse(status=401)

    if request.user.is_authenticated:
        context.update({"user": True})
        return render(request, "article_index.html", context)
    else:
        context.update({"user": False})
        return render(request, "article_index.html", context)


def article_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "article_category.html", context)


def article_detail(request, user_id, pk):
    try:
        user = User.objects.get(id=user_id)
        post = Post.objects.get(pk=pk, user=user)  # for exist post could be his user (/blog/@1/12)
        comments = Comment.objects.filter(post=post)
        context = {
            "comments": comments,
            "post": post,
            "user": user_id
        }

        if request.user.is_authenticated:
            form = CommentForm()
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = Comment(
                        author=form.cleaned_data["author"],
                        body=form.cleaned_data["body"],
                        post=post
                    )
                    comment.save()

            context.update({"form": form})
    except:
        return HttpResponse(status=401)

    return render(request, "article_detail.html", context)
