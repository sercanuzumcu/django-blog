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
import json




@csrf_exempt
def view_post(request, title_id):
    print request.POST
    message = ""
    if request.POST:
        yorum = request.POST.get('yorum', "")
        post_id = request.POST.get('post_id', "")
        title = request.POST.get('title', 1)
        body = request.POST.get('body', "")
        cevap = request.POST.get('cevap', "")
        yanit = request.POST.get('yanit', "")
        comment_id = request.POST.get('comment_id', "")
        b = Blog.objects.get(id=title_id)
        if yorum:
            c = Comment.objects.create(body=yorum)
            c.blog_set.add(b)
            c.save()
            message = u"Yorum Eklendi"
        elif title and body:
            b.title = title
            b.body = body
            b.save()
            message = u"Güncelleme Başarılı"
        elif yanit:
            a = Comment.objects.create(body=yanit)
            c2 = Comment.objects.get(id=comment_id)
            a.cevap.add(c2)
            a.save()
            message = u"Güncelleme Başarılı"

    else:
        b = Blog.objects.get(id=title_id)

    return render_to_response('view_post.html', {
        'post': b,
        'son_yazilanlar': Blog.objects.all()[:2],
        'comment': b.comment.filter().order_by('-pub_date')[:5],
        'message': message
    })


def view_category(request, title_id):

    return render(request, 'view_category.html', {
        'category': Category.objects.filter(id=title_id)[0],
        'son_yazilanlar': Blog.objects.order_by('-pub_date')[:3]


    })



def view_edit(request, title_id):
    print request.POST
    b = Blog.objects.get(id=title_id)
    if request.POST:
        b.title = request.POST.get('title', 1)
        b.body = request.POST.get('body', "")
        b.save()
    return render_to_response('view_edit.html', {'post': b})



