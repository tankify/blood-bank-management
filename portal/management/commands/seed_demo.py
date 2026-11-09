from django.core.management.base import BaseCommand
from portal.models import BloodBank, BloodCamp, BloodRequest, Donor

class Command(BaseCommand):
    help = "Load fictional records into the volatile demo database."
    def handle(self, *args, **options):
        if Donor.objects.exists():
            self.stdout.write("Demo records already loaded.")
            return
        Donor.objects.bulk_create([
            Donor(name="Demo Donor A", blood_group="O+", city="Varanasi", contact="0000000000"),
            Donor(name="Demo Donor B", blood_group="A-", city="Delhi", contact="0000000000"),
            Donor(name="Demo Donor C", blood_group="B+", city="Mumbai", contact="0000000000"),
            Donor(name="Demo Donor D", blood_group="AB+", city="Bengaluru", contact="0000000000"),
            Donor(name="Demo Donor E", blood_group="O-", city="Kolkata", contact="0000000000"),
        ])
        BloodRequest.objects.bulk_create([
            BloodRequest(requester_name="Demo Request A", blood_group="O+", city="Varanasi", contact="0000000000", units_needed=2),
            BloodRequest(requester_name="Demo Request B", blood_group="B+", city="Mumbai", contact="0000000000", units_needed=1),
            BloodRequest(requester_name="Demo Request C", blood_group="A-", city="Delhi", contact="0000000000", units_needed=3),
        ])
        BloodBank.objects.bulk_create([
            BloodBank(name="City Blood Centre", city="Varanasi", address="Demo address, Varanasi", contact="0000000000", demo_inventory_units=24),
            BloodBank(name="Central Blood Centre", city="Delhi", address="Demo address, Delhi", contact="0000000000", demo_inventory_units=18),
            BloodBank(name="Harbour Blood Centre", city="Mumbai", address="Demo address, Mumbai", contact="0000000000", demo_inventory_units=31),
        ])
        BloodCamp.objects.bulk_create([
            BloodCamp(name="Community Donation Day", city="Varanasi", address="Demo venue, Varanasi", contact="0000000000"),
            BloodCamp(name="City Donor Drive", city="Bengaluru", address="Demo venue, Bengaluru", contact="0000000000"),
        ])
        self.stdout.write(self.style.SUCCESS("Loaded fictional demo records."))
