from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm
from users.models import CustomUser


class UserRegisterView(View):
    def get(self, request):
        create_form = UserCreateForm
        return render(request, 'users/register.html', {'form':create_form})

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect("users:login")
        else:
            return render(request, 'users/register.html', {'form':create_form})


class UserLoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form':login_form})
    
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, 'You have successfully Logged in!')
            
            return redirect('landing_page')
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully Logged out!')
        return redirect('landing_page')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/edit-profile.html', {'form':user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES)

        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, 'You are successfully updated your profile!')
            return redirect('users:profile')
        return render(request, 'users/edit-profile.html', {'form': user_update_form})