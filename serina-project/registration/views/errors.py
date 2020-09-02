from django.shortcuts import render
from django.utils.translation import gettext as _


def error_400(request, *args, **kwargs):
    """Error view when a 400 error (Bad request) occurs."""

    image = "draw/void.svg"
    code = 400
    message = _("Your request has not been understood.")

    return render(request, 'registration/general/error.html', locals())

def error_403(request, *args, **kwargs):
    """Error view when a 403 error (Access forbidden) occurs."""

    image = "draw/access_denied.svg"
    code = 403
    message = _("You access to the requested page has been denied.")

    return render(request, 'registration/general/error.html', locals())

def error_404(request, *args, **kwargs):
    """Error view when a 404 error (Not found) occurs."""

    image = "draw/page_not_found.svg"
    code = 404
    message = _("The page you tried to reach does not exist.")

    return render(request, 'registration/general/error.html', locals())

def error_500(request, *args, **kwargs):
    """Error view when a 500 error (Server error) occurs."""

    image = "draw/server_down.svg"
    code = 500
    message = _("An internal server error occured on our side.")

    return render(request, 'registration/general/error.html', locals())
