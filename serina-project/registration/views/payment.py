from decimal import Decimal

from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from ..forms import PaymentForm


from django.utils.translation import ugettext as _

from ..models import ModuleRegistrationReport
from ..utils import messages as messages_utils


# Module Registration Report payments

def module_payment(request, pk):
    """Checkout view of the module registration request in order to proceed to
    a PayPal payment.

    Send the payment data to PayPal IPN in order for the user to procced to the
    payment.
    """

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)
    request.session['module_rr'] = module_rr.pk
    vat_excluded_price = round(module_rr.module.price / Decimal(1.21), 2)

    if module_rr.status != "APPROVED":
        messages_utils.module_not_payable(request)
        return redirect(module_rr.get_absolute_url())
    else:
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': module_rr.module.price,
            'item_name': _("Registration for {} to {}".format(
                module_rr.student_rr.created_by.get_full_name(),
                module_rr.module.title,
            )),
            'currency_code': 'EUR',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('module_payment_done')),
            'cancel_return': 'http://{}{}'.format(
                host,
                reverse('module_payment_cancelled'),
            ),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(
            request,
            'registration/payment/process_payment.html',
            {
                'module_rr': module_rr,
                'form': form,
                'vat_excluded_price': vat_excluded_price,
            },
        )


def get_module_rr_and_clean_session_pk(request):
    """Get the module registration instance based on the session variable
    stored and clean it."""

    module_rr_pk = request.session.get('module_rr')
    module_rr = ModuleRegistrationReport.objects.get(pk=module_rr_pk)

    del request.session['module_rr']

    return module_rr


@csrf_exempt
def module_payment_done(request):
    """Payement done view that flags the module registration request as 'PAYED'
    and redirect to the DetailView."""

    module_rr = get_module_rr_and_clean_session_pk(request)

    if module_rr.final_score:
        module_rr.status = "COMPLETED"
    else:
        module_rr.status = "PAYED"

    module_rr.save()

    messages_utils.module_payment_succeeded(request)

    return redirect(module_rr.get_absolute_url())


@csrf_exempt
def module_payment_cancelled(request):
    """Redirect the user to the module registration DetailView with a message
    indicating that the payment has failed."""

    module_rr = get_module_rr_and_clean_session_pk(request)

    messages_utils.module_payment_failed(request)

    return redirect(module_rr.get_absolute_url())


# Degree Registration Report payments

def degree_payment(request, pk):
    """Checkout view of the degree registration request in order to proceed to
    a PayPal payment.

    Send the payment data to PayPal IPN in order for the user to procced to the
    payment.
    """

    degree_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)
    request.session['module_rr'] = module_rr.pk
    vat_excluded_price = round(module_rr.module.price / Decimal(1.21), 2)

    if module_rr.status != "APPROVED":
        messages_utils.module_not_payable(request)
        return redirect(module_rr.get_absolute_url())
    else:
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': module_rr.module.price,
            'item_name': _("Registration for {} to {}".format(
                module_rr.student_rr.created_by.get_full_name(),
                module_rr.module.title,
            )),
            'currency_code': 'EUR',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('module_payment_done')),
            'cancel_return': 'http://{}{}'.format(
                host,
                reverse('module_payment_cancelled'),
            ),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(
            request,
            'registration/payment/process_payment.html',
            {
                'module_rr': module_rr,
                'form': form,
                'vat_excluded_price': vat_excluded_price,
            },
        )


def get_degree_rr_and_clean_session_pk(request):
    """Get the module registration instance based on the session variable
    stored and clean it."""

    module_rr_pk = request.session.get('module_rr')
    module_rr = ModuleRegistrationReport.objects.get(pk=module_rr_pk)

    del request.session['module_rr']

    return module_rr


@csrf_exempt
def degree_payment_done(request):
    """Payement done view that flags the module registration request as 'PAYED'
    and redirect to the DetailView."""

    module_rr = get_module_rr_and_clean_session_pk(request)

    if module_rr.final_score:
        module_rr.status = "COMPLETED"
    else:
        module_rr.status = "PAYED"

    module_rr.save()

    messages_utils.module_payment_succeeded(request)

    return redirect(module_rr.get_absolute_url())


@csrf_exempt
def degree_payment_cancelled(request):
    """Redirect the user to the module registration DetailView with a message
    indicating that the payment has failed."""

    module_rr = get_module_rr_and_clean_session_pk(request)

    messages_utils.module_payment_failed(request)

    return redirect(module_rr.get_absolute_url())