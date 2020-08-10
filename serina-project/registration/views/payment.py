from decimal import Decimal

from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from ..forms import PaymentForm
from ..models import ModuleRegistrationReport


def checkout(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            module_rr = cleaned_data["module_rr"]

            # TODO: Add payment date
            request.session['module_rr'] = module_rr.pk

            messages.add_message(request, messages.INFO, 'Order Placed!')
            return redirect('process_payment')


    else:
        form = PaymentForm()
        return render(request, 'registration/payment/checkout.html', {'form': form})


def process_payment(request):
    module_rr_pk = request.session.get('module_rr')
    module_rr = get_object_or_404(ModuleRegistrationReport, pk=module_rr_pk)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': module_rr.module.charge_price,
        'item_name': "{} for {} from {} to {}".format(
            module_rr.module.title,
            module_rr.student_rr.created_by.get_full_name(),
            module_rr.date_start,
            module_rr.date_end,
        ),
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(
        request,
        'registration/payment/process_payment.html',
        {'module_rr': module_rr, 'form': form},
    )


@csrf_exempt
def payment_done(request):
    return render(request, 'registration/payment/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'registration/payment/payment_cancelled.html')
