from django.shortcuts import render
from .models import Payment

def payment_page(request):
    payments = Payment.objects.all()
    return render(request, "payments.html", {"payments": payments})
