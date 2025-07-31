from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<int:item_id>/', item_detail, name='item-detail'),
    path('buy/<int:item_id>/', checkout_session, name='buy-item'),
    path('orders/<int:order_id>/', order_detail, name='order-detail'),
    path('payment/<int:order_id>/', create_payment, name='payment'),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
