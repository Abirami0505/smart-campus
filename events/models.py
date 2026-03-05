import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    points = models.IntegerField(default=10)
    registration_deadline = models.DateTimeField()

    def is_registration_open(self):
        return timezone.now() < self.registration_deadline

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True)
    total_points = models.IntegerField(default=0)

    BADGE_CHOICES = [
        ('None', 'No Badge'),
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
    ]

    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='None')

    def update_badge(self):
        if self.total_points >= 200:
            self.badge = 'Gold'
        elif self.total_points >= 100:
            self.badge = 'Silver'
        elif self.total_points >= 50:
            self.badge = 'Bronze'
        else:
            self.badge = 'None'
        self.save()

    def __str__(self):
        return self.user.username


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    qr_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    attended = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.event.name}"