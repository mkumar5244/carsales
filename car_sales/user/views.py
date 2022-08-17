from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from django.contrib import messages

from user.models import ContactUs
from user.forms import ContactUsForm, ContactUsAuthenticatedForm

class LoginView(View):

    form = AuthenticationForm()

    def get(self, request):
        return render(request, 'user/login.html', context={'form':self.form})

    def post(self, request):
        if 'username' not in request.POST.keys():
            messages.error(request, 'Missing username')
            return redirect('login')
        if 'password' not in request.POST.keys():
            messages.error(request, 'Missing password')
            return redirect('login')

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('user:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html', context={'form':self.form({'username':username})})

class LogoutView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'User already logged out')
        else:
            logout(request)
            messages.success(request, 'Logged out successfully')
        return redirect('home')

class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'user/register.html', context={'form':form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registered successfully')
            return redirect('user:dashboard')
        else:
            messages.error(request, 'Invalid data')
            return render(request, 'user/register.html', context={'form':form})

class ContactUsView(View):

    def get(self, request):
        form = ContactUsForm()
        return render(request, 'user/contact_us.html', context={'form':form})

    def post(self, request):
        data = request.POST.dict()
        user_auth = request.user.is_authenticated
        if user_auth:
            data.update(
                {
                    'email':request.user.email if request.user.email else ''
                }
            )
        form = ContactUsForm(data, request.FILES)
        if form.is_valid():
            query = form.save()
            if user_auth:
                query.user = request.user
                query.save()
            messages.success(request, 'Successfully saved query')
            if user_auth:
                return redirect('user:dashboard')
            else:
                return redirect('contact-us')
        else:
            print(form.errors)
            messages.error(request, 'Invalid data')
            if user_auth:
                return redirect('user:dashboard')
            else:
                return render(request, 'user/contact_us.html', context={'form':form})

class HomeView(View):

    def get(self, request):
        return render(request, 'user/home.html')

class DashboardView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login')
            return redirect('user:login')
        queries = ContactUs.objects.filter(user=request.user)
        form = ContactUsAuthenticatedForm()
        return render(request, 'user/dashboard.html', context={'form':form, 'queries': queries})