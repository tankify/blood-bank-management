from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from .models import BloodRequest, Donor

class PortalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def test_home_renders_dashboard_and_seed_data(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blood, when")
        self.assertContains(response, "Demo Donor A")

    def test_donor_filters_match_group_and_city(self):
        response = self.client.get(reverse("donors"), {"group": "O+", "city": "Varanasi"})
        self.assertContains(response, "Demo Donor A")
        self.assertNotContains(response, "Demo Donor B")

    def test_request_filters_match_group_and_city(self):
        response = self.client.get(reverse("requests"), {"group": "O+", "city": "Varanasi"})
        self.assertContains(response, "Demo Request A")
        self.assertNotContains(response, "Demo Request B")

    def test_donor_form_requires_login(self):
        response = self.client.get(reverse("register_donor"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_demo_donor(self):
        user = User.objects.create_user(username="demo-user", password="DemoPass!234")
        self.client.force_login(user)
        response = self.client.post(reverse("register_donor"), {
            "name": "New Demo Donor", "blood_group": "A+", "city": "Delhi", "contact": "0000000000"})
        self.assertRedirects(response, reverse("donors"))
        self.assertTrue(Donor.objects.filter(name="New Demo Donor").exists())

    def test_logged_in_user_can_add_demo_request(self):
        user = User.objects.create_user(username="demo-user", password="DemoPass!234")
        self.client.force_login(user)
        response = self.client.post(reverse("create_request"), {
            "requester_name": "Demo Patient", "blood_group": "O-", "city": "Mumbai",
            "contact": "0000000000", "units_needed": "2"})
        self.assertRedirects(response, reverse("requests"))
        self.assertTrue(BloodRequest.objects.filter(requester_name="Demo Patient").exists())

    def test_invalid_phone_is_rejected(self):
        user = User.objects.create_user(username="demo-user", password="DemoPass!234")
        self.client.force_login(user)
        response = self.client.post(reverse("register_donor"), {
            "name": "Invalid Demo", "blood_group": "O+", "city": "Delhi", "contact": "not-a-phone"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Donor.objects.filter(name="Invalid Demo").exists())
