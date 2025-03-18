
from ninja import Schema

# ================================================================
# 🔹 Payment Schemas
# ================================================================

class InitiatePaymentSchema(Schema):
    total: float
    reservation_code: str
    first_name: str
    last_name: str
    phone: str
    payment_method: str  # "paystack" or "flutterwave"