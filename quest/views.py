from datetime import date as date_cls, timedelta

from django.contrib import messages
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
    """Create or edit the log for any past day (default: today). Use ?date=YYYY-MM-DD."""
    today = timezone.localdate()
    raw = request.GET.get("date")

    if raw:
        try:
            log_date = date_cls.fromisoformat(raw)
        except ValueError:
            messages.error(request, "That date wasn't valid, so here is today instead.")
            return redirect("log_entry")
        if log_date > today:
            messages.error(request, "You can't log a day that hasn't happened yet.")
            return redirect("log_entry")
    else:
        log_date = today

    entry = DailyEntry.objects.filter(user=request.user, date=log_date).first()

    if request.method == "POST":
        form = DailyEntryForm(request.POST, instance=entry)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.date = log_date
            obj.save()
            messages.success(request, f"Saved your log for {log_date:%A, %d %B %Y}.")
            return redirect("dashboard" if log_date == today else "history")
    else:
        form = DailyEntryForm(instance=entry)

    context = {
        "form": form,
        "today": today,
        "log_date": log_date,
        "is_today": log_date == today,
        "entry": entry,
    }
    return render(request, "quest/log_form.html", context)


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
