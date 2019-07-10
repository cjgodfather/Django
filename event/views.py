from django.shortcuts import render, get_object_or_404, redirect
from event.models import Event, Ticket, Cart, OrderedTicket, Address
from django.utils import timezone
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.views import View
from django.core.paginator import Paginator
from .forms import TicketForm, UserRegisterForm, AddressForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout



User = get_user_model()


# Create your views here.

# try to user class-based view
# class EventListView(ListView):
#     template_name = "event/event_list.html"
#     model = Event
#     paginate_by = 10

#     def get_queryset(self, *args, **kwargs):
#         try:
#             form = SearchForm(self.request.GET)
#             print(form)
#         except:
#             event_qs = 
#             return event_qs

#     def get_context_data(self, **kwargs):
        
#         context = super().get_context_data(**kwargs)
#         context['search_form'] = search_form
#         return context

def event_list_view(request):
    previously_viewed_slug = request.session.get("event_viewed")
    user_viewed = request.session.get("user")
    try:
        viewed_item = Event.objects.get(slug=previously_viewed_slug)
    except ObjectDoesNotExist:
        viewed_item = None
        print("no previously viewed item")
    event_qs = Event.objects.all()
    name = request.GET.get("name")
    date = request.GET.get("date")
    location = request.GET.get("location")
    category = request.GET.get("category")
    free = request.GET.get("free")

    if name != "" and name is not None:
        event_qs = event_qs.filter(name__icontains=name)
    
    if date != "" and date is not None:
        event_qs = event_qs.filter(date__exact=date)

    if location != "" and location is not None:
        event_qs = event_qs.filter(location__exact=location)

    if category != "" and category is not None:
        event_qs = event_qs.filter(category=category)
    
    if free != "" and free is not None:
        event_qs = event_qs.filter(free=free)
    
    paginator = Paginator(event_qs, 5)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {"event_list":events, "viewed_item":viewed_item, "user_viewed":user_viewed}

    return render(request, "event/event_list.html", context)

def event_detail_view(request, slug):
    request.session['user'] = request.user.username
    request.session['event_viewed'] = slug
    event = get_object_or_404(Event, slug=slug)
    form = TicketForm

    try:
        tickets = Ticket.objects.filter(event=event)
    except ValueError:
        print("no tickets for this event yet")

    context = {"event": event, "tickets": tickets, "form": form}

    return render(request, "event/event.html", context)


def add_to_cart_view(request, slug):
    # get the ticket object
    event = get_object_or_404(Event, slug=slug)
    ticket_type = request.POST.get("ticket_type")
    ticket = get_object_or_404(Ticket, event=event, ticket_type=ticket_type)

    # get or create a ticket order
    ticket_form = TicketForm(request.POST)
    if ticket_form.is_valid():
        quantity = ticket_form.cleaned_data["quantity"]
        print(quantity)
    ordered_tickets, tickets_created = OrderedTicket.objects.get_or_create(
        user=request.user, ticket=ticket, quantity=quantity
    )

    # get the cart object
    cart_obj, cart_created = Cart.objects.get_or_create(user=request.user, ordered=False)
    print(cart_obj, cart_created)
    if not cart_created:
        if ordered_tickets in cart_obj.tickets.all():
            print("you already ordered the tickets")
            # cart_obj.tickets.quantity += quantity
            return redirect("event:cart")
        else:
            cart_obj.tickets.add(ordered_tickets)
            cart_obj.save()
    else:
        cart_obj.tickets.add(ordered_tickets)

    return redirect("event:detail", slug=slug)


class CartView(ListView):
    template_name = "event/cart.html"
    model = Cart
    
    def get_context_data(self, **kwargs):
        cart_qs = Cart.objects.filter(user=self.request.user)
        if cart_qs.exists():
            cart = cart_qs.first()
        context = super().get_context_data(**kwargs)
        context['ticket_list'] = cart.tickets.all()
        context['cart'] = cart
        return context


def delete_tickets_view(request):
    ticket = request.POST.get('ticket')
    cart_obj = Cart.objects.get(user=request.user)
    cart_obj.tickets.remove(ticket)
    return redirect("event:cart")

def user_register_view(request):
    register_form = UserRegisterForm(request.POST)
    if register_form.is_valid():
        username = register_form.cleaned_data['username']
        password = register_form.cleaned_data['password']
        email = register_form.cleaned_data['email']
        new_user = User(username=username, password=password, email=email)
        new_user.save()
        return redirect('event:list')

    context = {
        "register_form": register_form
    }
    return render(request, "event/register.html", context)

def user_login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("login successfully")
        return redirect('event:list')
    else:
        print("invalid username or password")


    return render(request, "event/login.html")

def user_logout_view(request):
    logout(request)
    return HttpResponse("you have logged out!")

def checkout_view(request):
    
    form = AddressForm(request.POST)
    if form.is_valid():
        street = form.cleaned_data['street']
        city= form.cleaned_data['city']
        state = form.cleaned_data['state']
        zip = form.cleaned_data['zip']
        country = form.cleaned_data['country']
        address_type = form.cleaned_data['address_type']
        new_address = Address(user=request.user, street=street, city=city, state=state, zip=zip, country=country, address_type=address_type)
        new_address.save()
        form = AddressForm()
        return redirect("event:payment")

    context = {
        'address_form': form,
    }
    return render(request, "event/checkout.html", context)

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "event/payment.html")