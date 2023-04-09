from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm , LoginForm
# Create your views here.

def loginuser(request):

    context = {
        'form' : LoginForm()
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            context['error'] = 'Invalid username or password'

    return render(request, 'account/login.html' , context)



def register(request):
    context = {
        'form' : RegisterForm()
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            repassword = form.cleaned_data.get('repassword')
            if password != repassword:
                context['error'] = 'Passwords do not match'
                context['form'] = form            
                return render(request , 'account/register.html' , context)

            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
        else:
            context['form'] = form
    return render(request , 'account/register.html' , context)