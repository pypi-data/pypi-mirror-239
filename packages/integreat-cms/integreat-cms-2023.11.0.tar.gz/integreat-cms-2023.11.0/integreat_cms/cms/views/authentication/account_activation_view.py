import logging

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from ...utils.account_activation_token_generator import (
    account_activation_token_generator,
)
from ...utils.translation_utils import gettext_many_lazy as __

logger = logging.getLogger(__name__)


class AccountActivationView(auth_views.PasswordResetConfirmView):
    """
    View to set a new password and activate and account.
    """

    #: The template which should be rendered
    template_name = "authentication/account_activation_form.html"
    #: If the password was successfully reset, redirect to the login
    success_url = reverse_lazy("public:login")
    #: The generator for activation tokens
    #: (use :class:`~integreat_cms.cms.utils.account_activation_token_generator.AccountActivationTokenGenerator` instead of the default one to
    #: make sure password reset tokens are not accepted for account activation and vice versa)
    token_generator = account_activation_token_generator

    def dispatch(self, *args, **kwargs):
        r"""
        The view part of the view. Handles all HTTP methods equally.

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict

        :return: The rendered template response or a redirection to the login page
        :rtype: ~django.template.response.TemplateResponse or ~django.http.HttpResponseRedirect
        """
        if self.request.user.is_authenticated:
            messages.success(
                self.request,
                _("You are already logged in."),
            )
            return redirect("public:region_selection")
        response = super().dispatch(*args, **kwargs)
        if isinstance(response, HttpResponseRedirect) or self.validlink:
            # If the link is valid, render the password reset confirm form (redirect means valid because the first step
            # is to store the token in a session variable and redirect to the generic [...]-activate-account/ url)
            return response
        # Redirect to the login form
        messages.error(
            self.request,
            __(
                _("This account activation link is invalid."),
                _("It may have already been used."),
                _(
                    "Please contact an administrator to request a new link to activate your account."
                ),
            ),
        )
        return redirect("public:login")

    def form_valid(self, form):
        """
        If the form is valid, show a success message.

        :param form: The supplied form
        :type form: ~django.contrib.auth.forms.SetPasswordForm

        :return: A redirection to the ``success_url``
        :rtype: ~django.http.HttpResponseRedirect

        """
        messages.success(
            self.request,
            __(
                _("Your account has been successfully activated."),
                _("You can now log in with your new password."),
            ),
        )
        form.user.is_active = True
        form.user.save()
        logger.info("Account activation for user %r was successful", form.user)
        return super().form_valid(form)
