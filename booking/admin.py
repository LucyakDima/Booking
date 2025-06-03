from booking.models import *
from django.contrib import admin
from .models import Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 5

class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'capacity', 'price', 'location')
    inlines = [RoomImageInline]
admin.site.register(Room, RoomAdmin)


admin.site.register(Booking)
# admin.site.register(Room)
