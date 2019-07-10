from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

# Create your models here.

User = get_user_model()

CATEGORY = (
    ("M", "MUSIC"),
    ("A", "ART"),
    ("P", "PARTY"),
    ("S", "SPORT"),
    ("B", "BUSINESS"),
)

TICKET_TYPE = (
    ("General admission", "GENERAL ADMISSION"),
    ("Early bird", "EARLY BIRD"),
    ("Children", "CHILDREN"),
    ("Senior", "SENIOR"),
)

ADDRESS_TYPE = (
    ("B", "BILLIING"),
    ("S", "SHIPPING"),
)


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    slug = models.SlugField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=1)
    description = models.CharField(max_length=1000)
    free = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event:detail", kwargs={"slug": self.slug})

    def add_to_cart_url(self):
        return reverse("event:add_to_cart", kwargs={"slug": self.slug})


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.ticket_type} ticket for {self.event.name}"


class OrderedTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="tickets")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} for {self.ticket}'

    def calculate_ticket_price(self):
        price = self.ticket.price * self.quantity
        return price

    def delete_ticket_url(self):
        return reverse("event:delete_ticket", kwargs={"ordered_ticket": self})


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_user")
    tickets = models.ManyToManyField(OrderedTicket, related_name="cart")
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} cart."

    def cart_total(self):
        total = 0
        for ticket in self.tickets.all():
            total += ticket.quantity * ticket.ticket.price
        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="address")
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=20)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE)

    def __str__(self):
        return f"{self.user.username} address"