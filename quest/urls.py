from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("log/", views.log_entry, name="log_entry"),
    path("history/", views.history, name="history"),
    path("plan/", views.plan, name="plan"),
    path("diet/", views.diet, name="diet"),
    path("signup/", views.signup, name="signup"),
]
