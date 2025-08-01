from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Item, Order
from django.http import JsonResponse, Http404, HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item.html', {
        'item': item,
        'price_dollars': item.price / 100,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_session(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'unit_amount': item.price,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://something.com/success',
        cancel_url='https://something.com/cancel',
    )

    return JsonResponse({'id': session.id})


def create_payment(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404("Order not found")

    amount = int(order.total_amount() * 100)
    currency = order.get_currency()
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        metadata={"order_id": order.id}
    )
    return JsonResponse({'clientSecret': intent.client_secret})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items_with_price = []
    for item in order.items.all():
        price_normal = item.item.price / 100
        items_with_price.append({
            'name': item.item.name,
            'quantity': item.quantity,
            'price': price_normal,
            'currency': item.item.currency,
        })

    total_normal = order.total_amount() / 100
    return render(request, "order.html", {
        "order": order,
        "items": items_with_price,
        "total": total_normal,
        "currency": order.get_currency(),
        "stripe_pub_key": settings.STRIPE_PUBLISHABLE_KEY,
    })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')

        try:
            order = Order.objects.get(pk=order_id)
            order.is_paid = True
            order.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)