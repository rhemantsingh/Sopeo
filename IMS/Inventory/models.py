from django.db import models
from datetime import datetime
import pytz
# Create your models here.


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    iin = models.CharField(unique=True, max_length=15, verbose_name="IIN")
    cost_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    selling_price = models.DecimalField(decimal_places=2, max_digits=10)
    profit_earned = models.DecimalField(decimal_places=2, max_digits=10)
    revenue = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Inventory:{self.id}--{self.name}--{self.iin}"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(cost_price__gte=0, selling_price__gte=0), name='Price must be Positive'),
            models.CheckConstraint(check=models.Q(selling_price__gt=models.F('cost_price')), name='Selling Price must be greater than Cost Price')

        ]

    def save(self, *args, **kwargs):
        self.profit_earned = self.quantity_sold * (self.selling_price - self.cost_price)
        self.revenue = self.quantity_sold * self.cost_price
        return super().save(*args, **kwargs)


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_cost = models.DecimalField(decimal_places=2, max_digits=10)
    order_date = models.DateTimeField(default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'))
    is_received = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='Positive Quantity')

        ]

    def __str__(self):
        return f"Order:{self.id}--{self.item}"

    def save(self, *args, **kwargs):
        self.order_cost = self.quantity * self.item.cost_price
        return super().save(*args, **kwargs)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_date = models.DateTimeField(datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y:%m:%d %H:%M:%S'))

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='Positive_Quantity')

        ]

    def __str__(self):
        return f"Transaction: {self.id}--{self.item}--{self.quantity}--{self.selling_price}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
