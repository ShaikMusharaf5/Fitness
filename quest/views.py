from datetime import timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import DailyEntryForm
from .models import DailyEntry, Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    today = timezone.localdate()
    entry = DailyEntry.objects.filter(user=request.user, date=today).first()

    week_start = today - timedelta(days=today.weekday())
    week_days = [week_start + timedelta(days=i) for i in range(7)]
    entries_by_date = {
        e.date: e
        for e in DailyEntry.objects.filter(user=request.user, date__gte=week_start, date__lte=today)
    }
    week_data = [
        {"date": d, "points": entries_by_date[d].points if d in entries_by_date else 0}
        for d in week_days
    ]
    week_points = sum(d["points"] for d in week_data)

    context = {
        "today": today,
        "entry": entry,
        "week_data": week_data,
        "week_points": week_points,
        "max_week_points": 40 * 7,
    }
    return render(request, "quest/dashboard.html", context)


@login_required
def log_entry(request):
    today = timezone.localdate()
    entry = DailyEntry.objects.filter(user=request.user, date=today).first()

    if request.method == "POST":
        form = DailyEntryForm(request.POST, instance=entry)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date = today
            obj.save()
            return redirect("dashboard")
    else:
        form = DailyEntryForm(instance=entry)

    return render(request, "quest/log_form.html", {"form": form, "today": today, "entry": entry})


@login_required
def history(request):
    entries = DailyEntry.objects.filter(user=request.user)
    paginator = Paginator(entries, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "quest/history.html", {"page_obj": page_obj})


def plan(request):
    return render(request, "quest/plan.html")


def diet(request):
    return render(request, "quest/diet.html")
