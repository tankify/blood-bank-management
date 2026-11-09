from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from urllib.parse import urlencode
from .forms import BloodRequestForm, DonorForm, RegistrationForm
from .models import BloodBank, BloodCamp, BloodGroup, BloodRequest, City, Donor

def filters_for(request):
    return {"group": request.GET.get("group", "").strip(), "city": request.GET.get("city", "").strip()}

def apply_filters(queryset, filters):
    if filters["group"] in BloodGroup.values:
        queryset = queryset.filter(blood_group=filters["group"])
    if filters["city"] in City.values:
        queryset = queryset.filter(city=filters["city"])
    return queryset

def home(request):
    filters = filters_for(request)
    return render(request, "portal/home.html", {
        "donor_count": Donor.objects.filter(is_available=True).count(),
        "request_count": BloodRequest.objects.count(),
        "bank_count": BloodBank.objects.count(),
        "donors": apply_filters(Donor.objects.filter(is_available=True), filters)[:4],
        "requests": apply_filters(BloodRequest.objects.all(), filters)[:4],
        "filters": filters, "blood_groups": BloodGroup.choices, "cities": City.choices,
    })

def donors(request):
    filters = filters_for(request)
    return render(request, "portal/donors.html", {
        "donors": apply_filters(Donor.objects.filter(is_available=True), filters),
        "filters": filters, "blood_groups": BloodGroup.choices, "cities": City.choices,
    })

def requests(request):
    filters = filters_for(request)
    return render(request, "portal/requests.html", {
        "requests": apply_filters(BloodRequest.objects.all(), filters),
        "filters": filters, "blood_groups": BloodGroup.choices, "cities": City.choices,
    })

@login_required
def register_donor(request):
    form = DonorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        donor = form.save()
        messages.success(request, f"Thanks, {donor.name}. Your demo profile was added.")
        return redirect("donors")
    return render(request, "portal/form.html", {"form": form, "title": "Become a donor",
        "eyebrow": "DONOR REGISTRATION", "submit_label": "Add demo profile"})

@login_required
def create_request(request):
    form = BloodRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save()
        messages.success(request, f"Your demo request for {item.blood_group} was added.")
        return redirect("requests")
    return render(request, "portal/form.html", {"form": form, "title": "Request blood",
        "eyebrow": "BLOOD REQUEST", "submit_label": "Add demo request"})

def banks(request):
    query = request.GET.get("q", "").strip()
    items = BloodBank.objects.all()
    if query:
        items = items.filter(Q(city__icontains=query) | Q(name__icontains=query))
    return render(request, "portal/banks.html", {"banks": items, "query": query})

def camps(request):
    query = request.GET.get("q", "").strip()
    items = BloodCamp.objects.all()
    if query:
        items = items.filter(Q(city__icontains=query) | Q(name__icontains=query))
    return render(request, "portal/camps.html", {"camps": items, "query": query})

def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your temporary demo account is ready.")
        return redirect("home")
    return render(request, "portal/form.html", {"form": form, "title": "Create account",
        "eyebrow": "TEMPORARY DEMO ACCOUNT", "submit_label": "Create account"})

@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("home")


# Approximate city-centre coordinates only. Fictional listings are not pinned.
CITY_CENTERS = {
    "Varanasi": (25.3176, 82.9739),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
}

def map_search(request):
    city = request.GET.get("city", "").strip()
    if city not in City.values:
        city = ""
    center = CITY_CENTERS.get(city)
    map_src = None
    if center:
        lat, lon = center
        bbox = f"{lon - 0.14},{lat - 0.11},{lon + 0.14},{lat + 0.11}"
        map_src = "https://www.openstreetmap.org/export/embed.html?" + urlencode({
            "bbox": bbox, "layer": "mapnik", "marker": f"{lat},{lon}",
        })
    banks = BloodBank.objects.filter(city=city) if city else BloodBank.objects.all()
    camps = BloodCamp.objects.filter(city=city) if city else BloodCamp.objects.all()
    return render(request, "portal/map_search.html", {
        "city": city, "cities": City.choices, "map_src": map_src,
        "banks": banks, "camps": camps,
    })
