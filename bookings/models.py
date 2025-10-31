import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Booking(models.Model):
	"""Guest booking capturing stay details and optional airport transfer."""

	ROOM_TYPE_CHOICES = [
		("single", "Single Room"),
		("master", "Master Room"),
		("meeting", "Meeting Room"),
		("deluxe", "Deluxe Room"),
		("executive", "Executive Room"),
		("suite", "Luxury Suite"),
	]
	ROOM_TYPE_RATES = {
		"single": 5000,
		"master": 9000,
		"meeting": 10000,
		"deluxe": 8000,
		"executive": 12000,
		"suite": 15000,
	}
	AIRPORT_CHARGE = 7000
	STATUS_CHOICES = [
		("pending", "Pending"),
		("confirmed", "Confirmed"),
		("cancelled", "Cancelled"),
	]

	booking_reference = models.CharField(max_length=12, unique=True, editable=False)
	full_name = models.CharField(max_length=100)
	cnic = models.CharField(
		max_length=15,
		validators=[RegexValidator(r"^[0-9\-]{13,15}$", "Enter a valid CNIC number.")],
	)
	address = models.TextField()
	email = models.EmailField(blank=True)
	phone_number = models.CharField(max_length=20, blank=True)
	room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
	room = models.ForeignKey(
		"core.Room",
		on_delete=models.SET_NULL,
		related_name="bookings",
		null=True,
		blank=True,
	)
	booking_days = models.PositiveSmallIntegerField(
		default=1, validators=[MinValueValidator(1), MaxValueValidator(7)]
	)
	airport_pick_drop = models.BooleanField(default=False)
	total_price = models.PositiveIntegerField(default=0)
	status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["booking_reference"]),
		]

	def __str__(self) -> str:
		return f"{self.booking_reference} - {self.full_name}"

	@classmethod
	def generate_reference(cls) -> str:
		return uuid.uuid4().hex[:12].upper()

	@property
	def base_rate(self) -> int:
		if self.room and self.room.price:
			return int(self.room.price)
		return self.ROOM_TYPE_RATES.get(self.room_type, 0)

	@property
	def airport_charge(self) -> int:
		return self.AIRPORT_CHARGE if self.airport_pick_drop else 0

	def calculate_total(self) -> int:
		return (self.base_rate * self.booking_days) + self.airport_charge

	def assign_room(self):
		"""Pick the first available room matching the type if none selected."""
		if self.room_id:
			return
		from core.models import Room

		available_room = Room.objects.filter(room_type=self.room_type, is_available=True).order_by("number").first()
		if available_room:
			self.room = available_room

	def update_room_availability(self):
		from core.models import Room

		if not self.room_id:
			return
		if self.status == "cancelled":
			Room.objects.filter(pk=self.room_id).update(is_available=True)
		else:
			Room.objects.filter(pk=self.room_id).update(is_available=False)

	def save(self, *args, **kwargs):
		is_new = self.pk is None
		if not self.booking_reference:
			self.booking_reference = self.generate_reference()
		self.assign_room()
		self.total_price = self.calculate_total()
		super().save(*args, **kwargs)
		# Update availability outside the initial save to avoid race conditions if no room found
		if is_new or "status" in (kwargs.get("update_fields") or []):
			self.update_room_availability()
		elif self.status != "cancelled":
			self.update_room_availability()

	def cancel(self):
		self.status = "cancelled"
		self.save(update_fields=["status", "updated_at"])
