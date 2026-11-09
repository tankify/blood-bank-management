import django.core.validators
from django.db import migrations, models

CITY_CHOICES = [("Varanasi", "Varanasi"), ("Delhi", "Delhi"), ("Mumbai", "Mumbai"), ("Bengaluru", "Bengaluru"), ("Kolkata", "Kolkata"), ("Hyderabad", "Hyderabad"), ("Other", "Other")]
GROUP_CHOICES = [("A+", "A positive"), ("A-", "A negative"), ("B+", "B positive"), ("B-", "B negative"), ("AB+", "AB positive"), ("AB-", "AB negative"), ("O+", "O positive"), ("O-", "O negative")]
PHONE = [django.core.validators.RegexValidator(message="Enter a valid phone number.", regex="^\\+?[0-9 ()-]{7,18}$")]

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="BloodBank", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=140)), ("city", models.CharField(choices=CITY_CHOICES, max_length=80)),
            ("address", models.CharField(max_length=220)), ("contact", models.CharField(max_length=18, validators=PHONE)),
            ("demo_inventory_units", models.PositiveSmallIntegerField(default=0))],
            options={"ordering": ["city", "name"]}),
        migrations.CreateModel(name="BloodCamp", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=140)), ("city", models.CharField(choices=CITY_CHOICES, max_length=80)),
            ("address", models.CharField(max_length=220)), ("contact", models.CharField(max_length=18, validators=PHONE)),
            ("event_date", models.DateField(blank=True, null=True))],
            options={"ordering": ["event_date", "city"]}),
        migrations.CreateModel(name="BloodRequest", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("requester_name", models.CharField(max_length=100)), ("blood_group", models.CharField(choices=GROUP_CHOICES, max_length=3)),
            ("city", models.CharField(choices=CITY_CHOICES, max_length=80)), ("contact", models.CharField(max_length=18, validators=PHONE)),
            ("units_needed", models.PositiveSmallIntegerField(default=1)), ("created_at", models.DateTimeField(auto_now_add=True))],
            options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="Donor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100)), ("blood_group", models.CharField(choices=GROUP_CHOICES, max_length=3)),
            ("city", models.CharField(choices=CITY_CHOICES, max_length=80)), ("contact", models.CharField(max_length=18, validators=PHONE)),
            ("is_available", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True))],
            options={"ordering": ["-created_at", "name"]}),
        migrations.AddIndex(model_name="bloodrequest", index=models.Index(fields=["blood_group", "city"], name="portal_bloodreq_group_city")),
        migrations.AddIndex(model_name="donor", index=models.Index(fields=["blood_group", "city", "is_available"], name="portal_donor_group_city_avail")),
    ]
