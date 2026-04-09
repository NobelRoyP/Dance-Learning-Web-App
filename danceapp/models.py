from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(null=True,blank=True,unique=True)
    age=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(null=True, upload_to='images/',blank=True)
    address=models.TextField(null=True,blank=True, max_length=200)
    GENDER_CHOICES = [
        ('M','Male'),
        ('F','female'),
        ('O','others'),
    ]
    Gender=models.CharField(max_length=10,null=True,blank=True)
    batch_time=models.CharField(max_length=100,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    course = models.ForeignKey('Courses', on_delete=models.SET_NULL, null=True, blank=True)
    is_joined_institution = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

from django.db import models

class Trainer(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    image = models.ImageField(upload_to='images/', null=True, blank=True)
    certificate = models.ImageField(upload_to='images/', null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    Gender = models.CharField(max_length=10, null=True, blank=True)

    phone = models.CharField(null=True, blank=True)
    experiance = models.IntegerField(null=True, blank=True)
    course = models.ForeignKey('Courses', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    password = models.CharField(max_length=200,null=True,blank=True)
    logo = models.ImageField(upload_to='institution_logos/', null=True, blank=True)
    address = models.TextField(null=True,blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    location=models.CharField(max_length=200,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

class Artist(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='makeup_profile/', null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)


class Shop(models.Model):
    

    # Basic Personal Details
    sname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    # Profile Photo
    shop_logo = models.ImageField(upload_to='customer_profile/', null=True, blank=True)

    # Location Details
    address = models.TextField(null=True, blank=True)
    # Account Security
    password = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.sname




class Product(models.Model):

    institution = models.ForeignKey(
        'Institution',
        on_delete=models.CASCADE,
        related_name='products',
        null=True, blank=True
    )

    # Basic Product Details
    product_name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    CATEGORY_CHOICES = [
        ('Dress', 'Dance Dress'),
        ('Ornament', 'Dance Ornament'),
        ('Accessory', 'Dance Accessory'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )

    DANCE_FORM_CHOICES = [
        ('Bharatanatyam', 'Bharatanatyam'),
        ('Mohiniyattam', 'Mohiniyattam'),
        ('Kuchipudi', 'Kuchipudi'),
        ('Kathak', 'Kathak'),
        ('Odissi', 'Odissi'),
        ('Manipuri', 'Manipuri'),
        ('Other', 'Other'),
    ]
    dance_form = models.CharField(
        max_length=50,
        choices=DANCE_FORM_CHOICES,
        null=True,
        blank=True
    )

    # Size & Fit Details (mainly for dresses)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)

    # Rental Details
    rental_price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Product Image
    product_image = models.ImageField(
        upload_to='product_images/',
        null=True,
        blank=True
    )

    # Description
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    # Status
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
from django.db import models



class MakeupReference(models.Model):

    DANCE_CATEGORIES = [
        ('Bharatanatyam', 'Bharatanatyam'),
        ('Mohiniyattam', 'Mohiniyattam'),
        ('Kuchipudi', 'Kuchipudi'),
    ]

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='makeup_references'
    )

    dance_category = models.CharField(
        max_length=50,
        choices=DANCE_CATEGORIES
    )

    image = models.ImageField(
        upload_to='makeup_references/'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.artist.name} - {self.dance_category}"



class Photos(models.Model):
    artist = models.ForeignKey(Artist,on_delete=models.CASCADE,related_name='photos',null=True,blank=True)
    DANCE_FORM_CHOICES = [
        ('Bharatanatyam', 'Bharatanatyam'),
        ('Mohiniyattam', 'Mohiniyattam'),
        ('Kuchipudi', 'Kuchipudi'),
     ]
    dance_category=models.CharField( max_length=50,choices=DANCE_FORM_CHOICES,null=True,blank=True)
    makeup_Reference_image=models.ImageField(upload_to='product_images/',null=True,blank=True)
    makeup_notes=models.CharField(null=True,blank=True, max_length=50)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Courses(models.Model):
    course_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class InstitutionTrainer(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='trainers')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='institutions')
    created_at = models.DateTimeField(auto_now_add=True)

class JoinInstitution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_institutions')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='members')
    is_applied = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

class Reel(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='reels', null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    video = models.FileField(upload_to='reels/', null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    


from django.utils import timezone
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    time_marked = models.TimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    class Meta:
        # This prevents a user from having two attendance records on the same day
        unique_together = ('user', 'date') 

    def __str__(self):
        return f"{self.user.name} - {self.date}"
    
class PaymentRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} - {'Success' if self.is_successful else 'Pending'}"


class Message(models.Model):
    sender_user    = models.ForeignKey(User,    on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    sender_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    receiver_user    = models.ForeignKey(User,    on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    receiver_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    content    = models.TextField()
    timestamp  = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender = self.sender_user or self.sender_trainer
        return f"{sender} → {self.timestamp:%H:%M}"
    

class CostumeBooking(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('paid', 'Paid'),
        ('returned', 'Returned'),
    ]

    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    product      = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookings')
    from_date    = models.DateField()
    to_date      = models.DateField()
    total_days   = models.PositiveIntegerField()
    rental_total = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total  = models.DecimalField(max_digits=10, decimal_places=2)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at    = models.DateTimeField(auto_now_add=True)
    notes        = models.TextField(blank=True, null=True)
    quantity     = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user.name} → {self.product.product_name} ({self.from_date} - {self.to_date})"


class BookingPayment(models.Model):
    booking            = models.OneToOneField(CostumeBooking, on_delete=models.CASCADE, related_name='payment')
    user               = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id  = models.CharField(max_length=100, unique=True)
    razorpay_payment_id= models.CharField(max_length=100, blank=True, null=True)
    amount             = models.IntegerField()          # in rupees
    is_successful      = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} — ₹{self.amount} — {'Paid' if self.is_successful else 'Pending'}"
