from django.contrib import admin
from .models import  Room, Booking, RoomImage, CustomUser

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('user__username', 'room__number')

admin.site.register(Booking, BookingAdmin)
admin.site.register(RoomImage)
admin.site.register(Room, RoomAdmin) 
admin.site.register(CustomUser)