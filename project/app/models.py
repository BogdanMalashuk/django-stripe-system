from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(help_text="Price in cents") 
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(help_text="Discount amount in cents")

    def __str__(self):
        return f"{self.name} (-{self.amount / 100:.2f})"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(help_text="Tax amount in cents")

    def __str__(self):
        return f"{self.name} (+{self.amount / 100:.2f})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def total_amount(self):
        total = sum(item.total_price() for item in self.items.all())
        if self.discount:
            total -= self.discount.amount
        if self.tax:
            total += self.tax.amount
        return max(total, 0)

    def get_currency(self):
        first_item = self.items.first()
        if first_item:
            return first_item.item.currency
        return 'usd'

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item.price * self.quantity / 100

    def __str__(self):
        return f"{self.quantity} × {self.item.name}"
