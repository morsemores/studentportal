from django.contrib import admin

from .models import Event, EventCertificate, EventRegistration, OrganizerProfile


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'phone', 'created_at')
    search_fields = ('user__username', 'organization_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'event_date', 'location', 'capacity', 'is_published')
    search_fields = ('title', 'location', 'category', 'organizer__username')
    list_filter = ('category', 'is_published', 'event_date')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registered_at')
    list_filter = ('status', 'event')
    search_fields = ('user__username', 'event__title')


@admin.register(EventCertificate)
class EventCertificateAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'uploaded_at')
    list_filter = ('event',)
    search_fields = ('event__title', 'user__username')
