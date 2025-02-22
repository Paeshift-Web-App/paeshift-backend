from django.http import HttpResponse
from django.urls import path
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")  # ✅ Redirect logged-in users correctly
    return redirect("/accounts/login/") # ✅ Redirect root to login page



@login_required  # ✅ Ensures only logged-in users can access the dashboard
def dashboard(request):
    return render(request, "dashboard.html")