from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.urls import reverse

from bookings.models import Booking
from .forms import ContactForm
from .models import Review, Room, Service

HOTEL_TOTAL_ROOMS = 50
HOME_HEADER_GALLERY = [
    {
        "title": "Meeting Room",
        "subtitle": "Executive boardroom seating with seamless AV integration",
        "image": "images/Meeting Room.jpg",
        "price": 10000,
    },
    {
        "title": "Standard Room",
        "subtitle": "Calming city-view sanctuaries for solo travellers",
        "image": "images/S Room.1.jpg",
        "price": 5000,
    },
    {
        "title": "Deluxe Room",
        "subtitle": "Spacious interiors with bespoke amenities",
        "image": "images/D Room.1.jpg",
        "price": 8000,
    },
    {
        "title": "Executive Room",
        "subtitle": "Panoramic skyline views and dedicated workspace",
        "image": "images/E Area.1.jpg",
        "price": 12000,
    },
    {
        "title": "Suites",
        "subtitle": "Signature suites curated for extended, indulgent stays",
        "image": "images/S Room.3.jpg",
        "price": 15000,
    },
]
DEFAULT_SERVICES = [
    {
        "name": "Complimentary Wi-Fi",
        "description": "Unlimited high-speed connectivity across every floor and public lounge.",
        "icon": "fa-solid fa-wifi",
        "price": None,
    },
    {
        "name": "Signature Breakfast",
        "description": "A curated buffet of continental and local delicacies, freshly prepared each morning.",
        "icon": "fa-solid fa-utensils",
        "price": None,
    },
    {
        "name": "Housekeeping & Laundry",
        "description": "Express laundry and evening turndown services for effortless comfort.",
        "icon": "fa-solid fa-soap",
        "price": None,
    },
    {
        "name": "24/7 Room Service",
        "description": "Attentive concierge assistance and gourmet in-room dining around the clock.",
        "icon": "fa-solid fa-bell-concierge",
        "price": None,
    },
    {
        "name": "Wellness & Gym Studio",
        "description": "Complimentary access to our fully equipped fitness suite and yoga pavilion.",
        "icon": "fa-solid fa-dumbbell",
        "price": None,
    },
    {
        "name": "Valet Parking",
        "description": "Secure basement parking with electric vehicle charging stations.",
        "icon": "fa-solid fa-square-parking",
        "price": None,
    },
    {
        "name": "Infinity Pool",
        "description": "Temperature-controlled pool with skyline views and private cabanas.",
        "icon": "fa-solid fa-person-swimming",
        "price": None,
    },
]
ROOM_COLLECTIONS = [
    {
        "slug": "meeting-room",
        "title": "Executive Meeting Room",
        "icon": "fa-solid fa-people-group",
        "summary": "Soundproof corporate suites with ergonomic seating, seamless conferencing tech, and on-call butler service for refreshments.",
        "price": 10000,
        "images": ["images/Meeting Room.jpg"],
    },
    {
        "slug": "bath-room",
        "title": "Bath Room Retreats",
        "icon": "fa-solid fa-bath",
        "summary": "Marble-clad bathrooms with rain showers, soaking tubs, and curated spa amenities for slow, restorative rituals.",
        "price": None,
        "images": ["images/B Room.1.jpg", "images/B Room.2.jpg", "images/B Room.3.jpg"],
    },
    {
        "slug": "standard-room",
        "title": "Standard Room",
        "icon": "fa-solid fa-bed",
        "summary": "Queen bedding, curated minibar selections, and soft ambient lighting perfect for leisure escapes.",
        "price": 5000,
        "images": ["images/S Room.1.jpg", "images/S Room.2.jpg", "images/S Room.3.jpg"],
    },
    {
        "slug": "deluxe-room",
        "title": "Deluxe Room",
        "icon": "fa-solid fa-champagne-glasses",
        "summary": "Expansive living area, bespoke furniture, and concierge-crafted turndown experiences.",
        "price": 8000,
        "images": ["images/D Room.1.jpg", "images/D Room.2.jpg", "images/D Room.3.jpg"],
    },
    {
        "slug": "executive-room",
        "title": "Executive Room",
        "icon": "fa-solid fa-briefcase",
        "summary": "Dedicated lounge access, smart workspace, and floor-to-ceiling views for discerning business travellers.",
        "price": 12000,
        "images": ["images/E Area.1.jpg", "images/E Area.2.jpg", "images/E Area.3.jpg"],
    },
    {
        "slug": "suites",
        "title": "Luxury Suites",
        "icon": "fa-solid fa-crown",
        "summary": "Private living quarters, bespoke concierge, and artful interiors curated for extended stays.",
        "price": 15000,
        "images": ["images/S Room.1.jpg", "images/S Room.2.jpg", "images/S Room.3.jpg"],
    },
]

EXTERIOR_GALLERY = [
    "images/E View.1.jpg",
    "images/E View.2.jpg",
    "images/E View.3.jpg",
    "images/E View.4.jpg",
    "images/E View.5.jpg",
    "images/E View.6.jpg",
]

RATING_RANGE = range(1, 6)


def _room_stats():
    """Return total, available and booked room counts."""
    total_rooms = HOTEL_TOTAL_ROOMS
    available_rooms = Room.objects.filter(is_available=True).count()
    booked_rooms = Room.objects.filter(is_available=False).count()
    return total_rooms, available_rooms, booked_rooms


def _hotel_context():
    return {
        "hotel_name": "HotelEase",
        "check_in": "Anytime (Welcome 24/7)",
        "check_out": "12 PM Fixed",
        "phone": "0307-2034454",
        "email": "mursaleenmalik286@gmail.com",
        "address": "Punjab University Employees Housing Society, Phase 2, Block A",
    }


def home(request):
    """HotelEase landing page with hero, highlights, and contact form."""
    total_rooms, available_rooms, booked_rooms = _room_stats()
    featured_services = list(Service.objects.filter(featured=True)[:6]) or DEFAULT_SERVICES
    spotlight_reviews = list(Review.objects.all()[:3])
    contact_form = ContactForm(request.POST or None)

    if request.method == "POST" and contact_form.is_valid():
        contact_form.save()
        messages.success(request, "Thank you for contacting HotelEase. Our team will reach out shortly.")
        return redirect(f"{reverse('core:home')}#contact")

    context = {
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "booked_rooms": booked_rooms,
        "hotel": _hotel_context(),
        "services": featured_services,
        "reviews": spotlight_reviews,
        "header_gallery": HOME_HEADER_GALLERY,
        "room_sections": ROOM_COLLECTIONS,
        "exterior_gallery": EXTERIOR_GALLERY,
        "rating_range": RATING_RANGE,
        "contact_form": contact_form,
    }
    return render(request, "core/home.html", context)


def rooms_view(request):
    rooms = Room.objects.all().order_by("room_type", "number")
    room_groups = []
    type_labels = dict(Room.ROOM_TYPES)
    for item in rooms.values("room_type").annotate(total=Count("id")):
        room_groups.append(
            {
                "code": item["room_type"],
                "label": type_labels.get(item["room_type"], item["room_type"].title()),
                "total": item["total"],
            }
        )
    total_rooms, available_rooms, booked_rooms = _room_stats()
    context = {
        "rooms": rooms,
        "room_groups": room_groups,
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "booked_rooms": booked_rooms,
        "hotel": _hotel_context(),
    }
    return render(request, "core/rooms.html", context)


def services_view(request):
    services_qs = list(Service.objects.all())
    services = services_qs or DEFAULT_SERVICES
    context = {
        "services": services,
        "hotel": _hotel_context(),
    }
    return render(request, "core/services.html", context)


def reviews_view(request):
    reviews = Review.objects.all()
    average_rating = reviews.aggregate(avg=Avg("rating"))
    avg_value = average_rating.get("avg") or 0 if average_rating else 0
    average_star_icons = []
    for star in RATING_RANGE:
        if avg_value >= star:
            average_star_icons.append("full")
        elif avg_value + 0.5 >= star:
            average_star_icons.append("half")
        else:
            average_star_icons.append("empty")
    context = {
        "reviews": reviews,
        "average_rating": round(avg_value, 1),
        "average_star_icons": average_star_icons,
        "rating_range": RATING_RANGE,
        "hotel": _hotel_context(),
    }
    return render(request, "core/reviews.html", context)


def contact_view(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for reaching out! We'll reply shortly.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form, "hotel": _hotel_context()})


@staff_member_required
def dashboard(request):
    """Simple dashboard summarising bookings and occupancy."""
    total_rooms, available_rooms, booked_rooms = _room_stats()
    bookings = Booking.objects.select_related("room").all()
    context = {
        "hotel": _hotel_context(),
        "total_rooms": total_rooms,
        "available_rooms": available_rooms,
        "booked_rooms": booked_rooms,
        "booking_count": bookings.count(),
        "recent_bookings": bookings[:10],
    }
    return render(request, "core/dashboard.html", context)
