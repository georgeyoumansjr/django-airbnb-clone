from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404
from rooms.models import Room
from rooms.forms import SearchForm, RoomForm
from reservations.forms import ReservationForm


class HomeView(ListView):
    """rooms application HomeView class
    Display list of room query set

    Inherit             : ListView
    Model               : Room
    paginate_by         : 10
    paginate_orphans    : 5
    ordering            : created_at
    context_object_name : rooms
    Templates name      : rooms/rooms_list.html
    """

    model = Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created_at"
    context_object_name = "rooms"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

        except Http404:
            return redirect(reverse("core:home"))


class RoomDetailView(DetailView):
    """rooms application RoomDetailView Class
    Display detail of room object

    Inherit             : DetailView
    Model               : Room
    Templates name      : rooms/room_detail.html
    """

    model = Room
    template_name = "rooms/room_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        # Add ReservationForm to the context
        reservation_form = ReservationForm()
        context["reservation_form"] = reservation_form

        return context
    
    def post(self, request, *args, **kwargs):
        room = self.object = self.get_object()
        reservation_form = ReservationForm(request.POST)

        if reservation_form.is_valid():
            check_in = reservation_form.cleaned_data["check_in"]
            check_out = reservation_form.cleaned_data["check_out"]

            # Check if the room is available for the selected dates
            if not room.is_booked(check_in, check_out):
                reservation = reservation_form.save(commit=False)
                reservation.guest = self.request.user
                reservation.room = room
                reservation.save()

                messages.success(request, "Reservation successful!")
                return redirect('rooms:detail', pk=room.pk)
            else:
                messages.error(request, "This room is already booked for the selected dates.")
        else:
            messages.error(request, "Invalid reservation details. Please check the form.")


        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
        

class SearchView(View):
    """rooms application SearchView Class
    Display list of rooms searched by city

    Inherit             : View
    Templates name      : rooms/search.html
    """

    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                is_superhost = form.cleaned_data.get("is_superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if is_superhost is True:
                    filter_args["host__is_superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                rooms = Room.objects.filter(**filter_args)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = SearchForm()

        return render(request, "rooms/search.html", {"form": form})


class RoomEditView(UpdateView):
    """rooms application RoomEditView Class
    Update room object fields data

    Inherit             : UpdateView
    Templates name      : rooms/room_edit.html
    """

    model = Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )


class RoomCreateView(CreateView):
    """rooms application RoomCreateView Class
    Create a new room object

    Inherit             : CreateView
    Model               : Room
    Form Class          : YourRoomForm
    Template name       : rooms/room_create.html  
    Success URL         : Redirects to the detail view of the created room
    """

    model = Room
    form_class = RoomForm  
    template_name = "rooms/room_create.html"  
    success_url = reverse_lazy("core:home")  
    
    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


