from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def registration(request):
    ufo=Userform()
    pfo=Profileform()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=Userform(request.POST)
        pfd=Profileform(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            MUPDO=pfd.save(commit=False)
            MUPDO.user=MUFDO
            MUPDO.save()
            send_mail('Registration',
                      'Hallow This is Yadhav Prasanth ... Nice to meet You',
                      'sarumoni1604@gmail.com',[MUFDO.email],fail_silently=False)
            return HttpResponse('Registration is successfully')
        else:
            return HttpResponse('Registration is not done successfully')

    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid data')
    return render(request,'user_login.html')


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(user=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)


@login_required
def change_password(request):

    if request.method=='POST':
        pw=request.POST['password']

        un=request.session.get('username')
        UO=User.objects.get(username=un)

        UO.set_password(pw)
        UO.save()
        return HttpResponse('password is changed successfully')

    return render(request,'change_password.html')


def reset_password(request):

    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('user is not present in my DB')
        

        return HttpResponse('Reset password is done successfully')
    return render(request,'reset_password.html')


