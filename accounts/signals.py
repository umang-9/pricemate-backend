from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    if reset_password_token is None:
        return
    # send an e-mail to the user
    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        "first_name": reset_password_token.user.first_name,
        "password_reset_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("forgot_password:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }

    # render email text
    email_html_message = render_to_string("email/forgot_password_email.html", context)
    email_plaintext_message = render_to_string(
        "email/forgot_password_email.txt", context
    )

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@pricemate.com",
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
