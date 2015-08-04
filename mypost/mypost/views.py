#-*- coding: utf-8 -*- #
import json
from django.db.models import Q
from posts.models import Blog, Category, Comment, Friend, Userprofile
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError


@csrf_exempt
def index(request):
    # Search alanında istek varsa, arananı ekrana getirme işlemi
    results = Blog.objects.order_by('-pub_date')
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
    # Login işlemi için TextArea'ya yazılan text değerlerini değişkene atama
    # Değişkenlerin kontrol edilip doğrulanması ve user'a atanması
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        response_data = {}
        # Eğer doğrulanmış bir user ise login et ve mesaj:Başarılı
        if user is not None:
            print user.__dict__
            if user.is_authenticated:
                auth_login(request, user)
                response_data['result'] = True
                response_data['message'] = u"Kullanıcı Girişi Başarılı"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        # Doğrulanmamış bir user için JSON-HATA dön
            else:
                response_data['result'] = False
                response_data['message'] = u"Lütfen bilgilerinizi kontrol edin"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        response_data['result'] = False
        response_data[
            'message'] = u"Hatalı giriş. Lütfen bilgilerinizi kontrol edin"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception, e:
        print e
        response_data['result'] = False
        response_data['message'] = u"Hatalı işlem. Lütfen Tekrar Deneyin"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def logout(request):
    # Oturumu açık olan kullanıcıyı LOGOUT eder
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
        # Kullanıcı Kayıt Formuna yazılan değerleri al ve değişkenlere ata
        if request.POST:
            first_name = request.POST.get('first_name', "")
            last_name = request.POST.get('last_name', "")
            user_name = request.POST.get('user_name', "")
            email = request.POST.get('email', "")
            pass_word = request.POST.get('pass_word', "")
            pass_word2 = request.POST.get('pass_word2', "")
            response_data = {}
            if pass_word != pass_word2:
                # Şifreler aynı değilse HATA dön
                response_data['result'] = False
                response_data['message'] = u"Şifreler Eşleşmiyor"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                # Değilse, Bu değerlere sahip bir kullanıcı oluştur ve KAYDET
                user = User.objects.create_user(
                    user_name, email, pass_word, first_name=first_name, last_name=last_name)
                user.save()
                user.id
                print user.__dict__
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            html = "<html><body>HATA</body></html>"
            return HttpResponse(html)

        return HttpResponseRedirect("/")

    except Exception, e:
        print e
        html = "<html><body>HATA</body></html>"
        return HttpResponse(html)


def profile(request):
    # Eğer giriş yapmış bir user ise; user_id'sini al ve bilgilerini
    # profile.html'e dön
    if request.user.is_authenticated:
        current_user = request.user
        return render(request, 'profile.html', {
            'user': User.objects.get(id=current_user.id),
            'alluser' : User.objects.all()[:7],
            'son_yazilanlar': Blog.objects.order_by('-pub_date')[:3],
            'userprofile': current_user.userprofile_set.get()
        })


@csrf_exempt
def like(request):
    # Seçilen yorumun beğen butonuna tıklandığında, o id'nin like'ını bir
    # artır, db'ye kaydet
    if request.POST['selected_like']:
        selected_like = Comment.objects.get(
            id=request.POST.get('selected_like', ""))
        selected_like.like += 1
        selected_like.save()
        return HttpResponseRedirect("/")

@csrf_exempt
def addfriend(request):
    current_user = request.user
    eklenen_arkadas_id = request.POST.get('selected_friend', "")
    response_data = {}
    if request.POST['selected_friend'] and request.POST['selected_friend']  :
        eklenen_arkadas = User.objects.get(id=eklenen_arkadas_id)
        selected_friend, result = Friend.objects.get_or_create(arkadas=current_user,
            eklenen_arkadas = eklenen_arkadas)
        current_user.friend_set.add(selected_friend)
        current_user.save()
        response_data['result'] = True
        response_data['message'] = u"Arkadaş Eklendi"
    return HttpResponse(json.dumps(response_data), content_type="application/json")
