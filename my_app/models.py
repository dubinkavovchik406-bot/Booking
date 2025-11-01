from django.db import models
from booking_system import settings
# Create your models here.

class Room(models.Model):
    number = models.IntegerField()
    price = models.IntegerField()
    capacity = models.IntegerField(default=2)
    square = models.IntegerField(default=20)
    room_type = models.CharField(max_length=256, default="standart")
    description = models.TextField(default="")

    def __str__(self):
        return f"Room #{self.number}"

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["number"]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="orders")
    start_time = models.DateField()
    end_time = models.DateField()
    creations_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in Room #{self.room.number}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["creations_time"]
