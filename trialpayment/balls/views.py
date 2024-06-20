from django.shortcuts import render

# Create your views here.


def index (request):
    return render (request, 'index.html')




# views.py

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
from django.shortcuts import render
from django.http import JsonResponse
import razorpay
import json



client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))




# views.py


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        amount = 50000  # amount in paise
        currency = 'INR'
        payment_capture = '1'

        response = client.order.create(dict(amount=amount, currency=currency, payment_capture=payment_capture))
        order_id = response['id']
        
        return JsonResponse({
            'order_id': order_id,
            'key': settings.RAZORPAY_KEY_ID,
            'amount': amount
        })

    return render(request, 'create_order.html')



# views.py

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
            bytes(razorpay_order_id + "|" + razorpay_payment_id, 'utf-8'),
            hashlib.sha256
        ).hexdigest()

        if generated_signature == razorpay_signature:
            # Payment is successful, process accordingly
            return render(request, 'success.html')
        else:
            # Payment failed
            return render(request, 'failure.html')

    return render(request, 'failure.html')



# @csrf_exempt
# def payment_success(request):
#     if request.method == 'POST':
#         razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
#         razorpay_order_id = request.POST.get('razorpay_order_id', '')
#         razorpay_signature = request.POST.get('razorpay_signature', '')

#         generated_signature = hmac.new(
#             bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
#             bytes(razorpay_order_id + "|" + razorpay_payment_id, 'utf-8'),
#             hashlib.sha256
#         ).hexdigest()

#         if generated_signature == razorpay_signature:
#             # Payment is successful, process accordingly
#             return render(request, 'success.html')
#         else:
#             # Payment failed
#             return render(request, 'failure.html')

#     return render(request, 'failure.html')
