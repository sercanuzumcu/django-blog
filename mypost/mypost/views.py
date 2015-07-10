#-*- coding: utf-8 -*- #
import json
from django.db.models import Q
from posts.models import Blog, Category, Comment
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

@csrf_exempt
def index(request):
    results = Blog.objects.all()
    q = None
    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET.get('q', None)
    if q is not None:
        results = results.filter(
            Q(title__contains=q) | Q(body__contains=q) | Q(category__title__contains=q))

    return render_to_response('index.html', {
        'posts': results[:5],
        'son_yazilanlar': Blog.objects.order_by('-pub_date')[:3]

    }, context_instance=RequestContext(request))

@csrf_exempt
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        response_data = {}

        if user is not None:
            print user.__dict__
            if user.is_authenticated:
                auth_login(request, user)
                response_data['result'] = True
                response_data['message'] = u"Kullanıcı Girişi Başarılı"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                response_data['result'] = False
                response_data['message'] = u"Lütfen bilgilerinizi kontrol edin"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        response_data['result'] = False
        response_data['message'] = u"Hatalı giriş. Lütfen bilgilerinizi kontrol edin"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception, e:
        print e
        response_data['result'] = False
        response_data['message'] = u"Hatalı işlem. Lütfen Tekrar Deneyin"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/posts")

def view_hakkimda(request):

    return render(request, 'view_hakkimda.html', {
        'son_yazilanlar': Blog.objects.order_by('-pub_date')[:3]
    })

@csrf_exempt
def signup(request):
    print request.POST
    try:
        if request.POST:
            first_name = request.POST.get('first_name', "")
            last_name = request.POST.get('last_name', "")
            user_name = request.POST.get('user_name', "")
            email = request.POST.get('email', "")
            pass_word = request.POST.get('pass_word' , "")
            pass_word2 = request.POST.get('pass_word2' , "")
            response_data = {}
            if pass_word != pass_word2:
                response_data['result'] = False
                response_data['message'] = u"Şifreler Eşleşmiyor"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                user = User.objects.create_user(user_name, email, pass_word, first_name = first_name,last_name=last_name)
                user.save()
                print user.__dict__
                return HttpResponse(json.dumps(response_data), content_type="application/json")        
        else:
            html="<html><body>HATA</body></html>"
            return HttpResponse(html)

        return HttpResponseRedirect("/")

    except Exception,e:
        print e
        html="<html><body>HATA</body></html>"
        return HttpResponse(html)
