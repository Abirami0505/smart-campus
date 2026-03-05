from django.contrib import admin
from .models import Event, Registration, Profile
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'email', 'event', 'registered_at', 'attended')

    def attendance_button(self, obj):
        if not obj.attended:
            url = reverse('mark_attendance', args=[obj.id])
            return format_html('<a class="button" href="{}">Mark Present</a>', url)
        return "Already Marked"

    attendance_button.short_description = "Attendance"


admin.site.register(Event)
admin.site.register(Profile)

    