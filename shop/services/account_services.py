from shop.services.all_moduls_for_service import *
import urllib


def send_verification_mail(user):
    title = 'Shop account verification'
    message = render_to_string('shop/email_verification.html', {'name': user.get_full_name(),
                                                                'DOMAIN': DOMAIN,
                                                                'id': user.id,
                                                                'token': urllib.parse.quote_plus(user.password)})
    send_mail(title, "", 'demediuk.smtp@gmail.com', ['demedyuk.v.i@gmail.com'], html_message=message)


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
