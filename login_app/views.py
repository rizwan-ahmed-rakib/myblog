from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from login_app.forms import SignUpForm, ChangeProfile, ProfilePic
from django.contrib.auth.models import User
from login_app.models import UserProfile


# Create your views here.
def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form': form, 'registered': registered}
    return render(request, 'Login_app/signup.html', context=dict)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'My_blog/home.html')
            # return HttpResponseRedirect(reverse('my_blog:home'))

    return render(request, 'Login_app/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('my_blog:blog_list'))


@login_required
def profile(request):
    return render(request, 'Login_app/profile.html', context={})


@login_required
def profile_change(request):
    current_user = request.user
    form = ChangeProfile(instance=current_user)
    if request.method == 'POST':
        form = ChangeProfile(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = ChangeProfile(instance=current_user)

    return render(request, 'Login_app/change_profile.html', context={'form': form})


@login_required
def password_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'Login_app/pass_change.html', context={'form': form, 'changed': changed})


@login_required
def add_profile_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_object = form.save(commit=False)
            user_object.user = request.user
            user_object.save()
            return HttpResponseRedirect(reverse('Login_App:profile'))
    return render(request, 'Login_app/add_profile_pic.html', context={'form': form})


@login_required
def change_profile_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login_App:profile'))
    return render(request, 'Login_app/add_profile_pic.html', context={'form': form})

def user_profile(request, username):
    view_user = User.objects.get(username=username)
    try:
        view_user_profile = UserProfile.objects.get(user=view_user)
    except UserProfile.DoesNotExist:
        view_user_profile = None
    
    context = {
        'view_user': view_user,
        'view_user_profile': view_user_profile,
    }
    return render(request, 'Login_app/user_profile.html', context)