import redis
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import (ProfileImagesForm, UserLoginForm, UserRegisterForm,
                    UserUpdateForm)
from .models import Profile
from .services import UserProfileServicesMixin, get_user

# redis connect
redis_obj = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB,
                              decode_responses=True)


class Login(LoginView):
    template_name = 'users/user.html'
    form_class = UserLoginForm


async def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if await sync_to_async(form.is_valid)():
            cd = form.cleaned_data
            await sync_to_async(form.save)()
            user = await get_user(cd["username"])
            await sync_to_async(Profile.objects.create)(user=user)
            redis_obj.set(f"{user}_subscription_type", "default")
            return redirect('users:user')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        profileForm = ProfileImagesForm(request.POST, request.FILES, instance=request.user.profile)
        apdateUserForm = UserUpdateForm(request.POST, instance=request.user)

        if profileForm.is_valid() and apdateUserForm.is_valid():
            apdateUserForm.save()
            profileForm.save()
            return redirect('users:profile')
    else:
        profileForm = ProfileImagesForm(instance=request.user.profile)
        apdateUserForm = UserUpdateForm(instance=request.user)

    data = {
        'profileForm': profileForm,
        'apdateUserForm': apdateUserForm,
    }

    return render(request, 'users/profile.html', data)


class UserProfileView(UserProfileServicesMixin, LoginRequiredMixin):
    model = User
    template_name = 'users/profile.html'
    form_class = UserUpdateForm
