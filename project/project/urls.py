from django.contrib import admin
from django.urls import path
from app.views import item_detail, create_checkout_session

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/<int:item_id>/', item_detail, name='item-detail'),
    path('buy/<int:item_id>/', create_checkout_session, name='buy-item'),
]
