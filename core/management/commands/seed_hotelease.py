from django.core.management.base import BaseCommand

from bookings.models import Booking
from core.models import Review, Room, Service


class Command(BaseCommand):
    help = "Seed the database with demo data for the HotelEase project."

    def handle(self, *args, **options):
        rooms_created = self._create_rooms()
        services_created = self._create_services()
        reviews_created = self._create_reviews()
        bookings_created = self._create_sample_booking()

        self.stdout.write(self.style.SUCCESS(
            "Seeding complete: "
            f"{rooms_created} rooms, "
            f"{services_created} services, "
            f"{reviews_created} reviews, "
            f"{bookings_created} booking."
        ))

    def _create_rooms(self) -> int:
        room_specs = [
            {
                "number": "101",
                "room_type": "single",
                "price": 5000,
                "description": "Calming standard room with city view, indulgent bedding, and writing desk.",
                "amenities": [
                    "Complimentary breakfast",
                    "50\" Smart TV",
                    "High-speed Wi-Fi",
                    "Rain shower",
                ],
            },
            {
                "number": "201",
                "room_type": "master",
                "price": 9000,
                "description": "Elegant master bedroom with lounge seating and curated minibar selection.",
                "amenities": [
                    "Private balcony",
                    "Executive desk",
                    "Luxury toiletries",
                    "Evening turndown",
                ],
            },
            {
                "number": "301",
                "room_type": "meeting",
                "price": 10000,
                "description": "Boardroom-style meeting suite with integrated conferencing technology.",
                "amenities": [
                    "16-seat board table",
                    "4K presentation display",
                    "Complimentary refreshments",
                    "Dedicated concierge support",
                ],
            },
            {
                "number": "401",
                "room_type": "deluxe",
                "price": 8000,
                "description": "Spacious deluxe room featuring statement lighting and custom furnishings.",
                "amenities": [
                    "Lounge seating",
                    "Walk-in wardrobe",
                    "Premium linen set",
                    "Rain shower & soaking tub",
                ],
            },
            {
                "number": "402",
                "room_type": "executive",
                "price": 12000,
                "description": "Executive skyline room with private workspace and club lounge access.",
                "amenities": [
                    "Panoramic skyline view",
                    "Ergonomic workstation",
                    "Complimentary lounge access",
                    "24/7 butler service",
                ],
            },
            {
                "number": "501",
                "room_type": "suite",
                "price": 15000,
                "description": "Signature suite with private living room, bespoke art, and curated amenities.",
                "amenities": [
                    "Private living room",
                    "In-room dining table",
                    "Spa-inspired bathroom",
                    "Personal concierge",
                ],
            },
        ]

        created = 0
        for spec in room_specs:
            _, was_created = Room.objects.update_or_create(
                number=spec["number"], defaults={key: value for key, value in spec.items() if key != "number"}
            )
            created += int(was_created)
        return created

    def _create_services(self) -> int:
        service_specs = [
            {
                "name": "24/7 Concierge",
                "icon": "fa-solid fa-bell-concierge",
                "description": "Dedicated concierge team ready to curate your stay around the clock.",
                "price": None,
            },
            {
                "name": "Luxury Spa & Sauna",
                "icon": "fa-solid fa-spa",
                "description": "Holistic spa rituals blending aromatherapy and deep tissue relaxation techniques.",
                "price": 12000,
            },
            {
                "name": "Airport Transfers",
                "icon": "fa-solid fa-car-side",
                "description": "Executive chauffeur transfers to and from the airport in luxury sedans.",
                "price": 8500,
            },
            {
                "name": "Gourmet Dining",
                "icon": "fa-solid fa-utensils",
                "description": "Seasonal tasting menus crafted by award-winning chefs.",
                "price": 9500,
            },
        ]

        created = 0
        for spec in service_specs:
            _, was_created = Service.objects.update_or_create(
                name=spec["name"],
                defaults={key: value for key, value in spec.items() if key != "name"},
            )
            created += int(was_created)
        return created

    def _create_reviews(self) -> int:
        review_specs = [
            {
                "name": "Amina Q.",
                "rating": 5,
                "comment": "Every detail felt thoughtful and premium. The booking concierge made our anniversary unforgettable!",
                "location": "Karachi, PK",
            },
            {
                "name": "Daniel R.",
                "rating": 4,
                "comment": "Spacious rooms with breathtaking views. The spa treatment was exceptional.",
                "location": "Dubai, UAE",
            },
            {
                "name": "Sophia L.",
                "rating": 5,
                "comment": "Loved the personalized airport transfer and seamless check-in experience.",
                "location": "London, UK",
            },
        ]

        created = 0
        for spec in review_specs:
            _, was_created = Review.objects.update_or_create(
                name=spec["name"],
                comment=spec["comment"],
                defaults={key: value for key, value in spec.items() if key not in {"name", "comment"}},
            )
            created += int(was_created)
        return created

    def _create_sample_booking(self) -> int:
        room = Room.objects.filter(is_available=True).order_by("number").first()
        if not room:
            return 0

        booking, created = Booking.objects.get_or_create(
            email="guest@example.com",
            defaults={
                "full_name": "Test Guest",
                "cnic": "42101-1234567-1",
                "address": "123 Beach Avenue, Karachi",
                "phone_number": "03001234567",
                "room_type": room.room_type,
                "booking_days": 3,
                "airport_pick_drop": True,
                "notes": "Please arrange a fruit basket on arrival.",
            },
        )

        if booking.room_id is None:
            booking.room = room
            booking.save()
        return int(created)
