#-*- coding: utf-8 -*- #
from posts.models import Blog
from posts.models import Category
from posts.models import Comment
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext


@csrf_exempt
def view_post(request, title_id):
    # POST GÖSTERME VIEW
    print request.POST
    message = ""
    if request.POST and request.user.is_authenticated:
        yorum = request.POST.get('yorum', "")
        post_id = request.POST.get('post_id', "")
        title = request.POST.get('title', 1)
        body = request.POST.get('body', "")
        cevap = request.POST.get('cevap', "")
        yanit = request.POST.get('yanit', "")
        comment_id = request.POST.get('comment_id', "")

        blogs = Blog.objects.get(id=title_id)
        # YORUM EKLEME
        if yorum:
            comment = Comment.objects.create(body=yorum)
            comment.blog_set.add(blogs)
            comment.save()
            message = u"Yorum Eklendi"
        # POST DÜZENLEME
        elif title and body:
            blogs.title = title
            blogs.body = body
            blogs.save()
            message = u"Güncelleme Başarılı"
        # YORUMA YORUM EKLEME
        elif yanit:
            comment_a = Comment.objects.create(body=yanit)
            comment_c = Comment.objects.get(id=comment_id)
            comment_a.cevap.add(comment_c)
            comment_a.save()
            message = u"Güncelleme Başarılı"

    else:
        blogs = Blog.objects.get(id=title_id)
        current_user = 1
    return render(request, 'view_post.html', {
        'post': blogs,
        'son_yazilanlar': Blog.objects.all()[:3],
        'comment': blogs.comment.filter().order_by('-pub_date')[:5],
        'message': message
    })


def view_category(request, title_id):
    # CATEGORY GÖSTERME VIEW
    current_user = request.user
    return render(request, 'view_category.html', {
        'category': Category.objects.filter(id=title_id)[0],
        'son_yazilanlar': Blog.objects.order_by('-pub_date')[:3]

    })


def view_edit(request, title_id):
    # POST DÜZENLEME VIEW
    print request.POST
    current_user = request.user
    blogs = Blog.objects.get(id=title_id)
    if request.POST:
        blogs.title = request.POST.get('title', 1)
        blogs.body = request.POST.get('body', "")
        blogs.save()
    return render(request, 'view_edit.html', {
        'post': blogs
    })
