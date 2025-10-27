from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Customer {self.name} {self.surname}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]

class Room(models.Model):
    number = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"Room #{self.number}"

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]
templates/base.html, templates/booking/order-form.html, templates/booking/room-detail.html, templates/booking/rooms-list.html

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="orders")
    start_time = models.DateField()
    end_time = models.DateField()
    creations_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} {self.customer.surname} in Room #{self.room.number}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["creations_time"]
