import logging
from email.mime.image import MIMEImage
from smtplib import SMTPAuthenticationError, SMTPException

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def send_mail(
    subject, email_template_name, html_email_template_name, context, recipient
):
    """
    Sends welcome email to user with new account.

    Making use of  :class:`~django.core.mail.EmailMultiAlternatives` and
    :class:`~email.mime.image.MIMEImage` to send a multipart email with plain text and html
    version and also attach the branding logo.

    :param subject: The subject of the email
    :type subject: str

    :param email_template_name: The template to be used to render the text email
    :type email_template_name: str

    :param html_email_template_name: The template to be used to render the HTML email
    :type html_email_template_name: str

    :param subject: The subject of the email
    :type subject: str

    :param context: The template context variables
    :type context: dict

    :param recipient: The email address of the recipient
    :type recipient: str
    """
    context.update(
        {
            "base_url": settings.BASE_URL,
            "COMPANY": settings.COMPANY,
            "BRANDING": settings.BRANDING,
            "BRANDING_TITLE": settings.BRANDING_TITLE,
        }
    )
    # Assemble message body
    body = render_to_string(
        email_template_name,
        context,
    )
    # Initialize message
    email = EmailMultiAlternatives(subject=subject, body=body, to=[recipient])
    email.mixed_subtype = "related"
    # Attach HTML email body
    html_message = render_to_string(html_email_template_name, context)
    email.attach_alternative(html_message, "text/html")
    # Attach logo
    if image_path := finders.find(
        f"logos/{settings.BRANDING}/{settings.BRANDING}-logo.png"
    ):
        with open(image_path, mode="rb") as f:
            image = MIMEImage(f.read())
            email.attach(image)
            image.add_header("Content-ID", "<logo>")
    else:
        logger.debug(
            "Logo not found at %s, will proceed without attaching.",
            finders.searched_locations,
        )
    # Send email
    try:
        email.send()
    except BadHeaderError as e:
        logger.error(e)
        raise RuntimeError(_("Malformed header data.")) from e
    except SMTPAuthenticationError as e:
        logger.error(e)
        raise RuntimeError(_("Invalid email credentials.")) from e
    except SMTPException as e:
        logger.error(e)
        raise RuntimeError(_("An SMTP error occured.")) from e
    except ConnectionRefusedError as e:
        logger.error(e)
        raise RuntimeError(_("The email server refused the connection.")) from e
