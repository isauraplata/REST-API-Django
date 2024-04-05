#paypal_integration/ views.py
from django.urls import reverse
import json
from orders.models import Order
import os
from dotenv import load_dotenv

load_dotenv()

def order_purchase(request, order_id):
    
    order = Order.objects.get(id=order_id)
    
    paypal_dict = {
        "business": os.environ.get('PAYPAL_EMAIL'),
        "amount": order.total_price,
        "item_name": order.dish,
        "invoice": order_id,
        'currency_code': 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
    }
    