from shop.services.all_moduls_for_service import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import urllib

def get_all_users():
    users = list()
    users_query_set = CustomUser.objects.all()
    for user in users_query_set:
        users.append({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                      'email': user.email, 'phone_number': user.phone_number,
                      'is_superuser': user.is_superuser})
    return users

def set_is_superuser(user_id: int, is_superuser: bool):
    user = CustomUser.objects.filter(pk=user_id)
    if user:
        print(is_superuser)
        user = user[0]
        user.is_superuser = is_superuser
        user.save()

def send_verification_mail(user):
    title = 'Shop account verification'
    message = render_to_string('shop/email/email_verification.html', {'name': user.get_full_name(),
                                                                'DOMAIN': DOMAIN,
                                                                'id': user.id,
                                                                'token': urllib.parse.quote_plus(user.password)})
    send_mail(title, "", 'demediuk.smtp@gmail.com', [user.email,], html_message=message)


def verify_user(id, token):
    is_verified = False
    user = CustomUser.objects.filter(pk=id)
    if user:
        user = user[0]
        if user.password == token:
            user.is_verified = True
            is_verified = True
            user.save()
    return is_verified


def send_password_reset_mail(email: str):
    user = CustomUser.objects.filter(email=email)
    if user:
        user = user[0]
        token_generator = PasswordResetTokenGenerator()
        user.reset_password_token = token_generator.make_token(user)
        user.save()
        title = 'Shop reset password'
        message = render_to_string('shop/email/email_password_reset.html', {'name': user.get_full_name(),
                                                                          'DOMAIN': DOMAIN,
                                                                          'id': user.id,
                                                                          'token': user.reset_password_token})
        send_mail(title, "", 'demediuk.smtp@gmail.com', [email,], html_message=message)


def is_correct_parameters_for_reset_password(id: int, token: str) -> bool:
    user = CustomUser.objects.filter(pk=id)
    if user:
        user = user[0]
        return user.reset_password_token == token
    else:
        return Fasle


def reset_password(id, password):
    user = CustomUser.objects.get(pk=id)
    try:
        validate_password(password=password, user=user)
    except ValidationError as err:
        return err
    user.set_password(password)
    user.reset_password_token = ""
    user.save()