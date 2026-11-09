from django.core.validators import RegexValidator
from django.db import models

PHONE_VALIDATOR = RegexValidator(r"^\+?[0-9 ()-]{7,18}$", "Enter a valid phone number.")

class BloodGroup(models.TextChoices):
    A_POSITIVE = "A+", "A positive"
    A_NEGATIVE = "A-", "A negative"
    B_POSITIVE = "B+", "B positive"
    B_NEGATIVE = "B-", "B negative"
    AB_POSITIVE = "AB+", "AB positive"
    AB_NEGATIVE = "AB-", "AB negative"
    O_POSITIVE = "O+", "O positive"
    O_NEGATIVE = "O-", "O negative"

class City(models.TextChoices):
    VARANASI = "Varanasi", "Varanasi"
    DELHI = "Delhi", "Delhi"
    MUMBAI = "Mumbai", "Mumbai"
    BENGALURU = "Bengaluru", "Bengaluru"
    KOLKATA = "Kolkata", "Kolkata"
    HYDERABAD = "Hyderabad", "Hyderabad"
    OTHER = "Other", "Other"

class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    city = models.CharField(max_length=80, choices=City.choices)
    contact = models.CharField(max_length=18, validators=[PHONE_VALIDATOR])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at", "name"]
        indexes = [models.Index(fields=["blood_group", "city", "is_available"])]
    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class BloodRequest(models.Model):
    requester_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    city = models.CharField(max_length=80, choices=City.choices)
    contact = models.CharField(max_length=18, validators=[PHONE_VALIDATOR])
    units_needed = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["blood_group", "city"])]
    def __str__(self):
        return f"{self.blood_group} request in {self.city}"

class BloodBank(models.Model):
    name = models.CharField(max_length=140)
    city = models.CharField(max_length=80, choices=City.choices)
    address = models.CharField(max_length=220)
    contact = models.CharField(max_length=18, validators=[PHONE_VALIDATOR])
    demo_inventory_units = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ["city", "name"]
    def __str__(self):
        return self.name

class BloodCamp(models.Model):
    name = models.CharField(max_length=140)
    city = models.CharField(max_length=80, choices=City.choices)
    address = models.CharField(max_length=220)
    contact = models.CharField(max_length=18, validators=[PHONE_VALIDATOR])
    event_date = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ["event_date", "city"]
    def __str__(self):
        return self.name
