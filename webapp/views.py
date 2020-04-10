from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *


# Create your views here.
class IndexView(View):

    template_name = 'index.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            context['username'] = request.user.username
        return render(request, self.template_name, context)


class SignupView(View):

    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, self.template_name)

    def post(self, request):
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            return HttpResponse('Must pass email')

        if 'password' in request.POST:
            password = request.POST['password']
        else:
            return HttpResponse('Must pass password')
        try:
            user = User.objects.create_user(username=email, is_active=False)
            user.set_password(password)
            user.save()
        except IntegrityError as err:
            print(err)
            return HttpResponse(err, status=400)
        else:
            return redirect('signin')



class SigninView(View):

    template_name = 'signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return render(request, self.template_name)

    def post(self, request):
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            return HttpResponse('Must pass email')

        if 'password' in request.POST:
            password = request.POST['password']
        else:
            return HttpResponse('Must pass password')

        try:
            account = User.objects.filter(username=email).first()

        except Exception as e:
            print(e)
            return HttpResponse(str(e))

        if account is None:
            return HttpResponse('There is no such account', status=404)
        elif account.is_active is False:
            return HttpResponse('Account not active, request approval from admin.', status=403)

        try:
            user = authenticate(request, username=email, password=password)
        except:
            return HttpResponse("USER DOES NOT EXIST!!!")

        if user is None:
            return redirect('signin')
        else:
            login(request, user)
            return redirect('dashboard')


class SignoutView(View):

    def get(self, request):
        logout(request)
        return redirect('signin')


class DashboardView(View):

    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username

        context = {
            'username': username
        }
        return render(request, self.template_name, context)


    @method_decorator(login_required)
    def post(self, request):
        UserData.objects.create(user=request.user, something=request.POST['something'], \
                        option1=int(request.POST['option-1']), option2=int(request.POST['option-2']), \
                        text=request.POST['textarea'])
        return redirect('thankyou')

class MyDataView(View):

    template_name = 'mydata.html'

    def get(self, request):
        user = request.user

        data = UserData.objects.filter(user=user).first()

        context = {
            'username': user.username,
            'something': data.something,
            'option1': data.option1,
            'option2': data.option2,
            'text': data.text
        }

        return render(request, self.template_name, context)



class ThankyouView(View):

    def get(self, request):
        return HttpResponse('Thank you!')