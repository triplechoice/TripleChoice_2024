from django.contrib import auth
from django.views import View
from django.shortcuts import resolve_url, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.forms import LoginForm, RegistrationForm, UserForm, UserProfileForm
from authentication.serilizers.user_serializer import UserSerializer
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login
from authentication.models import User, UserProfile
from authentication.token import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from authentication.email import send_activation_email, send_password_reset_email

from django.contrib.auth.forms import PasswordResetForm


class CustomerLoginView(auth_views.LoginView):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and (not user.is_superuser):
            return redirect('customer:customer_dashboard')

        return render(request, 'frontend/authentication/login.html', {"form": LoginForm})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        try:
            if request.POST.get('username') == "":
                messages.error(request, message='Email field is required', extra_tags='error')
                return render(request, 'frontend/authentication/login.html', {'form': form})

            if request.POST.get('password') == "":
                messages.error(request, message='Password field is required', extra_tags='error')
                return render(request, 'frontend/authentication/login.html', {'form': form})
            user = User.objects.get(email=request.POST.get('username'))
            if not user.is_active:
                messages.error(request,
                               message='Your account is not active. Please active you account from given email, Otherwise contact with admin',
                               extra_tags='error')
                return redirect('authentication:login')

            if user.check_password(request.POST.get('password')):
                login(request, user)
                url = self.request.GET.get('url')

                if url is not None:
                    if url.split('/')[1] == 'part':
                        return redirect(reverse('product:part.details', args=[url.split('/')[2]]))

                messages.success(request, 'Login successfully', extra_tags='success')
                return redirect('customer:customer_dashboard')
            messages.error(request, message='Credential not match', extra_tags='error')
            return render(request, 'frontend/authentication/login.html', {'form': form})
        except:
            messages.error(request, message='User not found', extra_tags='error')
            return redirect('authentication:login')

    def get_success_url(self):
        url = self.request.GET.get('url')
        if url is not None:
            if url.split('/')[1] == 'part':
                return resolve_url(reverse('product:part.details', args=[url.split('/')[2]]))
        # TODO::"set user url"
        return resolve_url(reverse('customer:customer_dashboard'))

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except Exception:
            raise None


class AuthCheckView(APIView):
    def get(self, request):
        try:
            user = auth.get_user(request)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception:
            raise Exception


class CustomerLogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('/')


class Profile(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_form = UserForm(instance=request.user)
            user_profile_form = UserProfileForm(instance=request.user.userprofile)
            profile = UserProfile.objects.get(user=request.user)
            context = {
                'user_form': user_form,
                'user_profile_form': user_profile_form,
                'profile': profile
            }
            return render(request, 'frontend/authentication/profile.html', context)
        return redirect('authentication:login')

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile successfully updated', extra_tags='success')
            return redirect('authentication:user_profile')


class RegistrationView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and (not user.is_superuser):
            return redirect('/user')

        form = RegistrationForm()
        return render(request, 'frontend/authentication/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
            send_activation_email(request, user)
            messages.success(request, 'We sent an email to activate your account ', extra_tags='success')
            return redirect('authentication:login')

        return render(request, 'frontend/authentication/registration.html', {'form': form})


def activateView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserExists(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(email=username).first()
        if not user:
            return Response({"success": "success"}, status=status.HTTP_200_OK)
        user = user.check_password(password)
        if user:
            return Response({"success": "success"}, status=status.HTTP_200_OK)
        return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)


class ApiLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is not None:
            if user.check_password(password):
                login(request, user)
                return Response({"is_logged_in": "logged_in"})
            else:
                return Response({"is_logged_in": "not_logged_in"})
        return Response({"is_logged_in": "no_user_found"})


class PassWordResetView(View):
    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()

        return render(request, "frontend/authentication/password_reset.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

        user = User.objects.filter(email=email).first()
        if user:
            send_password_reset_email(request, user)
            return redirect("password_reset_done")
        messages.error(request, message='User does not exist', extra_tags='error')
        return render(request, "frontend/authentication/password_reset.html", {"form": form})


class AdminPassWordResetView(View):
    def get(self, request, *args, **kwargs):
        form = PasswordResetForm()

        return render(request, "frontend/authentication/admin_password_reset.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

        user = User.objects.filter(email=email).first()
        if user:
            if user.is_superuser:
                send_password_reset_email(request, user)
                return redirect("password_reset_done")
        messages.error(request, message='User does not exist or user is not super User', extra_tags='error')
        return render(request, "frontend/authentication/admin_password_reset.html", {"form": form})
