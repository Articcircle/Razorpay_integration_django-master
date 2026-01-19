from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt

from .models import Coffee
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email= request.POST.get('email')
        client = razorpay.Client(auth =("rzp_test_S4xNQZHc9hnBbS" , "HU8Z8vqlkBxip2HNcXePTSqN"))
        payment = client.order.create({'amount':amount, 'currency':'INR',
                                       'payment_capture':'1' })
        
        coffee = Coffee(name = name , amount =amount,email=email , order_id = payment['id'])
        coffee.save()
        
        return render(request, 'index.html' ,{'payment':payment})
    return render(request, 'index.html')


@csrf_exempt
def success(request):
    if request.method == "POST":
        order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")

        user = Coffee.objects.filter(order_id=order_id).first()

        if user:
            user.razorpay_payment_id = payment_id
            user.paid = True
            user.save()

            # Email templates
            msg_plain = render_to_string('email.txt', {'name': user.name})
            msg_html = render_to_string('email.html', {'name': user.name})

            send_mail(
                subject="Your Donation is Successful",
                message=msg_plain,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=msg_html,
            )

    return render(request, "success.html")

