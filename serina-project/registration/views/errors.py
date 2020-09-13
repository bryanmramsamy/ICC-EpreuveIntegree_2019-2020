from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _


def error_400(request, *args, **kwargs):
    """Error view when a 400 error (Bad request) occurs."""

    image = 'void'
    code = 400
    code_text = _("Bad request")
    message = _("Your request has not been understood.")
    help_text = _("Unfortunalty, you tried to perform an action which has not "
                  "been understood by our servers.")
    support_mail = settings.CONTACT_MAILS["support"]

    return render(request, 'registration/general/error.html', locals(),
                  status=400)


def error_403(request, *args, **kwargs):
    """Error view when a 403 error (Access forbidden) occurs."""

    image = 'access_denied'
    code = 403
    code_text = _("Forbidden")
    message = _("Your access to the requested page has been denied.")
    help_text = _("Unfortunalty, you tried to perform an action your current "
                  "account permission level does not allow you to do.")
    support_mail = settings.CONTACT_MAILS["support"]

    return render(request, 'registration/general/error.html', locals(),
                  status=403)


def error_404(request, *args, **kwargs):
    """Error view when a 404 error (Not found) occurs."""

    image = 'page_not_found'
    code = 404
    code_text = _("Page not found")
    message = _("The page you tried to reach does not exist.")
    help_text = _("Unfortunalty, you tried to reach a page which does not "
                  "exist.")
    support_mail = settings.CONTACT_MAILS["support"]

    return render(request, 'registration/general/error.html', locals(),
                  status=404)


def error_500(request, *args, **kwargs):
    """Error view when a 500 error (Server error) occurs."""

    image = 'server_down'
    code = 500
    code_text = _("Server error")
    message = _("An internal server error occured on our side.")
    help_text = _("Unfortunalty, the action you tried to perform caused an "
                  "internal error on the servers side. We welcome you to "
                  "report this, by clicking on the button bellow, in order "
                  "for us to fix this bug as soon as possible. We appologies "
                  "for this incovenience.")
    support_mail = settings.CONTACT_MAILS["support"]

    return render(request, 'registration/general/error.html', locals(),
                  status=500)
