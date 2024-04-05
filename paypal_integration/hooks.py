# paypal_webhook

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import os
from dotenv import load_dotenv
from orders.models import Order

load_dotenv()

def handle_paypal_ipn(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Check if the receiver email matches
        if ipn_obj.receiver_email != os.environ.get('PAYPAL_EMAIL'):
            # Not a valid payment
            return
        
        # Check if the currency is USD
        if ipn_obj.mc_currency != 'USD':
            return
        
        #Update order status in database
        order = Order.objects.get(pk=ipn_obj.invoice)
        order.payment_status = 'paid'
        order.save()

            
valid_ipn_received.connect(handle_paypal_ipn)
