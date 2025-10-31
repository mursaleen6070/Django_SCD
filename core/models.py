from django.db import models


class Room(models.Model):
	"""Represents an individual room at HotelEase."""

	ROOM_TYPES = [
		("single", "Single Room"),
		("master", "Master Room"),
		("meeting", "Meeting Room"),
		("deluxe", "Deluxe Room"),
		("executive", "Executive Room"),
		("suite", "Luxury Suite"),
	]

	number = models.CharField(max_length=10, unique=True)
	room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default="single")
	price = models.PositiveIntegerField(help_text="Per night room rate in PKR", default=5000)
	description = models.TextField(blank=True)
	main_image = models.ImageField(upload_to="rooms/", blank=True, null=True)
	washroom_image = models.ImageField(upload_to="rooms/", blank=True, null=True)
	balcony_image = models.ImageField(upload_to="rooms/", blank=True, null=True)
	exterior_image = models.ImageField(upload_to="rooms/", blank=True, null=True)
	is_available = models.BooleanField(default=True)
	amenities = models.JSONField(default=list, blank=True, help_text="List of amenity strings")

	class Meta:
		ordering = ["number"]

	def __str__(self) -> str:
		return f"Room {self.number}"

	@property
	def status_label(self) -> str:
		return "Available" if self.is_available else "Booked"

	@property
	def room_type_label(self) -> str:
		return dict(self.ROOM_TYPES).get(self.room_type, self.room_type.title())


class Service(models.Model):
	"""Hotel amenity or service offered to guests."""

	name = models.CharField(max_length=120)
	icon = models.CharField(
		max_length=80,
		help_text="Font Awesome class, e.g. 'fa-solid fa-wifi'",
		default="fa-solid fa-star",
	)
	description = models.TextField()
	price = models.PositiveIntegerField(blank=True, null=True, help_text="Optional price in PKR")
	featured = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class Review(models.Model):
	"""Guest review with rating and optional photo."""

	RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

	name = models.CharField(max_length=120)
	photo = models.ImageField(upload_to="reviews/", blank=True, null=True)
	rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	location = models.CharField(max_length=120, blank=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"Review by {self.name}"


class ContactMessage(models.Model):
	"""Stores contact/feedback messages from website."""

	name = models.CharField(max_length=150)
	email = models.EmailField()
	subject = models.CharField(max_length=150)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	handled = models.BooleanField(default=False)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"Message from {self.name}"
