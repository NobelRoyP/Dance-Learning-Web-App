from django.contrib import admin
from .import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Trainer)
admin.site.register(models.Institution)
admin.site.register(models.JoinInstitution)
admin.site.register(models.PaymentRecord)
admin.site.register(models.Attendance)
admin.site.register(models.Product)
admin.site.register(models.BookingPayment)
admin.site.register(models.CostumeBooking)