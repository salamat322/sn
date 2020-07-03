from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse

from .forms import SignUpForm, ProfileUpdateForm
from .tokens import account_activation_token
from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            Profile.objects.create(user=user)
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(user.profile.get_absolute_url())
    else:
        return HttpResponse('Activation link is invalid!')


def profile(request, pk):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(profile.get_absolute_url())
    else:
        form = ProfileUpdateForm()
    return render(request, 'users/profile.html', locals())


def users_page(request):
    users = User.objects.all()
    return render(request, 'users/users.html', locals())


def follow_user(request, pk):
    profile_to_follow = get_object_or_404(Profile, pk=pk)
    profile = request.user.profile
    data = {}
    if profile_to_follow.follows.filter(id=profile.id).exists():
        data['message'] = "You are already following this user."
    else:
        profile_to_follow.follows.add(profile)
        #data['message'] = "You are now following {}".format(profile_to_follow)
    return render(request, 'users/users.html', locals())