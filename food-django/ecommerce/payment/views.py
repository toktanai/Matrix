from django.shortcuts import render,get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import order

from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def payment_done(request):
	return render(request,'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request,'payment/canceled.html')



def payment_process(request):
	order_id = request.session.get('order_id')
	orders = get_object_or_404(order, id=order_id)
	host = request.get_host()

	paypal_dict = {
		'business':settings.PAYPAL_RECEIVER_EMAIL,
		'amount': '%.2f' % orders.get_total_cost().quantize(Decimal('.01')),
		'item_name': 'Order {}'.format(order.id),
		'invoice': str(orders.id),
		'currency_code':'USD',
		'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		'return_url': 'http://{}{}'.format(host,reverse('payment:done')),
		'cancel_return': 'http://{}{}'.format(host,reverse('payment:canceled')),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {
	'order':orders,
	'form':form,
	}
	return render(request,'payment/process.html',context)
