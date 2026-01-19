from django.db import models
from django.core.exceptions import ValidationError


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    # order-related fields
    product_id = models.CharField(max_length=50, null=True, blank=True)
    order_day = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    customer_response = models.TextField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Rating between 0–5 only
    rating = models.PositiveSmallIntegerField(default=0)

    def clean(self):
        if self.status != 'Delivered' and self.delivered_date is not None:
            raise ValidationError("Delivered date can only be set when status is 'Delivered'.")

        if self.status != 'Delivered' and self.rating not in [0, None]:
            raise ValidationError("Rating can only be given after delivery.")

        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5.")

    def save(self, *args, **kwargs):
        # hard loop: if rating > 5, reset to 0 before saving
        if self.rating > 5:
            self.rating = 0
        elif self.rating < 0:
            self.rating = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
