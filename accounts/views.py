from django.contrib.auth import authenticate, get_user_model, login, logout

from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm

from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    return render(request, 'index.html', {})

def login_view(request):
    title = "Login"
    next = request.GET.get("next")
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("profile")

    return render(request, "login.html", {"form":form, "title":title})

def register_view(request):
    if request.user.is_authenticated():
        return redirect("profile")

    title = "Register"
    next = request.GET.get("next")
    form = UserRegisterForm(request.POST or None)
    print("start")
    if form.is_valid():
        print("valid")
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("profile")
    else:
        print("invalid")
    return render(request, "register.html", {"form": form, "title":title})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    form = UserProfileForm(request.POST or None, instance=user.profile)
    if form.is_valid():
        user.profile.save()

    return render(request, "profile.html", {"user": user, "form": form})

