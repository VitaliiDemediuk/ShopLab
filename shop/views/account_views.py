from shop.views.all_moduls_for_views import *
import shop.services.account_services as account_services
from shop.forms.account_forms import *
from django.contrib.auth import login, logout


def account(request):
    if request.method == "POST":
        if request.POST['operation'] == 'set_is_seperuser':
            user_id = int(request.POST['user_id'])
            is_superuser = True if request.POST['is_checked'] == 'true' else False
            account_services.set_is_superuser(user_id, is_superuser)
    if request.user.is_authenticated:
        sections = section_brand_service.get_sections_with_categories()
        users = account_services.get_all_users()
        return render(request, 'shop/account.html', {'sections': sections,
                                                     'users': users})
    else:
        return redirect('login')


def registration(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        form = RegistrationForm()
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                account_services.send_verification_mail(user)
                messages.success(request, 'Registration successful!')
                return redirect('login')
            else:
                messages.error(request, 'Registration failed!')
                messages.error(request, form.errors)
                form = RegistrationForm(request.POST)
        sections = section_brand_service.get_sections_with_categories()
        return render(request, 'shop/registration.html', {'sections': sections,
                                                      'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('account')
    else:
        if request.method == 'POST':
            form = UserLoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user.is_verified:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                else:
                    messages.error(request, 'Verify your email')
                    return redirect('login')
                return redirect('index')
            else:
                messages.error(request, 'Login failed!')
                messages.error(request, form.errors['__all__'])
                return redirect('login')
        else:
            form = UserLoginForm()
            sections = section_brand_service.get_sections_with_categories()
            return render(request, 'shop/login.html', {'sections': sections,
                                                       'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def email_verification(request):
    is_verified = account_services.verify_user(request.GET['id'], request.GET['token'])
    if is_verified:
        messages.success(request, 'Email verified!')
    return redirect('login')


def forgot_password(request):
    if request.user.is_authenticated:
        return HttpResponseNotFound()
    else:
        form = ForgotPasswordForm()
        if request.method == 'POST':
            form = ForgotPasswordForm(data=request.POST)
            if form.is_valid():
                data = form.cleaned_data
                account_services.send_password_reset_mail(data['email'])
                messages.success(request, "Instructions for resetting your password have been sent to your email.")
                return redirect('index')
            else:
                messages.error(request, form.errors['__all__'])
                return redirect('index')

        sections = section_brand_service.get_sections_with_categories()
        return render(request, 'shop/forgot-password.html', {'sections': sections,
                                                             'form': form})


def reset_password(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        id, token = None, None
        try:
            id = int(request.POST['id'])
            token = request.GET['token']
        except:
            messages.error(request, "Reset password error!")
            redirect('index')
        if not account_services.is_correct_parameters_for_reset_password(id, token):
            messages.error(request, "Reset password error!")
            return redirect('index')
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "The passwords are not the same!")
            return redirect((request.build_absolute_uri()))
        errs = account_services.reset_password(id, request.POST['password1'])
        if errs:
            for err in errs:
                messages.error(request, err)
            return redirect((request.build_absolute_uri()))
        else:
            messages.success(request, "The password reset!")
            return redirect('login')
    try:
        id = int(request.GET['id'])
        token = request.GET['token']
        if account_services.is_correct_parameters_for_reset_password(id, token):
            sections = section_brand_service.get_sections_with_categories()
            return render(request, 'shop/reset-password.html', {'sections': sections,
                                                                'form': form, 'id': id, 'token': token})
    except:
        pass
    return redirect('index')
