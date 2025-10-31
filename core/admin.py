from django.contrib import admin

from .models import ContactMessage, Review, Room, Service


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ("number", "room_type", "price", "is_available")
	list_filter = ("room_type", "is_available")
	search_fields = ("number", "description")
	readonly_fields = ("status_label",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("name", "featured", "price")
	list_filter = ("featured",)
	search_fields = ("name", "description")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("name", "rating", "created_at")
	list_filter = ("rating",)
	search_fields = ("name", "comment")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ("subject", "name", "email", "handled", "created_at")
	list_filter = ("handled",)
	search_fields = ("name", "email", "subject")
