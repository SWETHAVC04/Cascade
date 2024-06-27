import random
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .forms import CreateUserForm, LoginForm, CaptchaForm, OTPForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse

# -----------------------------------------------------Homepage view-----------------------------------------------
def homepage(request):
    return render(request, 'cascadeAuth/index.html')

# ------------------------------------------------------Register view-----------------------------------------------

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('cascadeAuth/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'your-email@example.com', [to_email])
            return redirect('confirmation')  # Redirect to the 'confirmation' URL name
    else:
        form = CreateUserForm()
    
    context = {'registerform': form}
    return render(request, 'cascadeAuth/register.html', context=context)

def confirmation(request):
    return render(request, 'cascadeAuth/confirmation.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('activation_success')
    else:
        return render(request, 'cascadeAuth/activation_invalid.html')

def activation_success(request):
    return render(request, 'cascadeAuth/activation_success.html')

def activation_invalid(request):
    return render(request, 'cascadeAuth/activation_invalid.html')
    
# -------------------------------------------------------Dashboard view-----------------------------------------------
@login_required(login_url="login")
def dashboard(request):
    return render(request, 'cascadeAuth/dashboard.html')
# --------------------------------------------------------Login view-----------------------------------------------
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['username'] = username
                request.session['password'] = password

                send_mail(
                    'OTP for login',
                    f'Your OTP is {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect("otp")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form data")

    context = {'form': form}
    return render(request, 'cascadeAuth/login.html', context=context)

# ----------------------------------------------------Forgot password view-----------------------------------------

def password_reset(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('resetPassword', kwargs={'uidb64': uid, 'token': token})
                )
                subject = "Password Reset Requested"
                message = render_to_string('cascadeAuth/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, "A password reset email has been sent.")
                return redirect('password_reset_done')  # Redirect to password reset done page
            except User.DoesNotExist:
                messages.error(request, "No user is registered with this email address.")
        else:
            messages.error(request, "Invalid email address.")

    context = {'form': form}
    return render(request, 'cascadeAuth/password_reset_form.html', context=context)

def resetPassword(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password1']
                confirm_password = form.cleaned_data['password2']
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('password_reset_complete')  # Redirect to password reset complete page
                else:
                    messages.error(request, "Passwords do not match.")
            else:
                messages.error(request, "Invalid form data.")
        else:
            form = ResetPasswordForm()

        context = {'form': form}
        return render(request, 'cascadeAuth/password_reset_confirm.html', context=context)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('password_reset') 

# -----------------------------------------------------OTP view---------------------------------------------------
def otp(request):
    form = OTPForm()
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')  # Use cleaned_data to get form field value safely
            sent_otp = request.session.get('otp')

            if str(entered_otp) == str(sent_otp):
                username = request.session.get('username')
                password = request.session.get('password')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    auth.login(request, user)
                    return redirect("captcha")
                else:
                    messages.error(request, "Invalid credentials. Please try again.")
            else:
                messages.error(request, "Invalid OTP. Please enter the correct OTP.")

    context = {'otp_form': form}
    return render(request, 'cascadeAuth/otp.html', context=context)

# ----------------------------------------------------Captcha view--------------------------------------------------
def captcha(request):
    form = CaptchaForm()
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
           if auth.get_user(request).is_authenticated and request.session.get('is_authenticated_with_otp', False):
                return redirect("dashboard")
           else:
                return redirect("dashboard")

    context = {'captcha_form': form}
    return render(request, 'cascadeAuth/captcha.html', context=context)

# -----------------------------------------Logout view-------------------------------------------
def logout(request):
    auth.logout(request)
    return redirect("homepage")