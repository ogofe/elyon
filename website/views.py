from django.shortcuts import render, redirect
from core.models import Message
# Create your views here.
def homepage_view(request):
    ctx = {
        'page_title': 'Home'
    }
    template = 'site/index.html'
    return render(request, template, ctx)


def place_order_view(request):
    ref = request.META['HTTP_REFERER']
    template = 'site/place-order.html'
    ctx = {
        'page_title': "Place an Order"
    }

    if request.method == "POST":
        data = request.POST
        msg = Message(
            sender_name=data['name'],
            sender_email=data['email'],
            message_subject=data['subject'],
            message_body=data['message'],
        )
        msg.save()
        return redirect(ref)
    
    return render(request, template, ctx)


def message_us_view(request):
    ref = request.META['HTTP_REFERER']

    if request.method == "POST":
        data = request.POST
        msg = Message(
            sender_name=data['name'],
            sender_email=data['email'],
            message_subject=data['subject'],
            message_body=data['message'],
        )
        msg.save()
    return redirect(ref)