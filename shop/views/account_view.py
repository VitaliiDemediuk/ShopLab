from shop.views.all_moduls_for_views import *
from shop.forms.account_forms import RegistrationForm, UserLoginForm
from django.contrib.auth import login, logout


def account(request):
    if request.user.is_authenticated:
        sections = section_brand_service.get_sections_with_categories()
        return render(request, 'shop/account.html', {'sections': sections,
                                                     'user': request.user})
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
                form.save()
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
                login(request, user)
                messages.success(request, 'Login successful!')
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