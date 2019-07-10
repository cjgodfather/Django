from django.contrib import admin
from event.models import Event, Ticket, Cart, OrderedTicket, Address


# Register your models here.

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Cart)
admin.site.register(OrderedTicket)
admin.site.register(Address)
