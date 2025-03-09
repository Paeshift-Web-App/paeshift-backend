from ninja import Schema
from datetime import datetime
from decimal import Decimal

# -------------------------------------------------------
# 1) Authentication Schemas
# -------------------------------------------------------
class LoginSchema(Schema):
    email: str
    password: str

class SignupSchema(Schema):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str


# -------------------------------------------------------
# 2) Job Schemas
# -------------------------------------------------------
class JobListSchema(Schema):
    id: int
    title: str
    description: str = None
    client_name: str
    status: str
    date: str = None
    time: str = None
    duration: str = None
    amount: Decimal = None
    image: str = None
    location: str = None
    date_posted: str
    no_of_application: int

class JobDetailSchema(JobListSchema):
    applicant_name: str = None
    payment_status: str


# -------------------------------------------------------
# 3) Application Schemas
# -------------------------------------------------------
class ApplicationListSchema(Schema):
    id: int
    job_id: int
    applicant_name: str
    is_accepted: bool
    applied_at: datetime


# -------------------------------------------------------
# 4) Saved Jobs Schema
# -------------------------------------------------------
class SavedJobSchema(Schema):
    id: int
    job_id: int
    title: str
    status: str
    date: str = None
    time: str = None
    duration: str = None
    amount: Decimal = None
    location: str = None
    saved_at: datetime


# -------------------------------------------------------
# 5) Payment Schema
# -------------------------------------------------------
class PaymentSchema(Schema):
    job_id: int
    total: Decimal  # Amount before deduction

class PaymentDetailSchema(Schema):
    id: int
    payer_name: str
    recipient_name: str = None
    original_amount: Decimal
    service_fee: Decimal
    final_amount: Decimal
    payment_status: str
    created_at: datetime


# -------------------------------------------------------
# 6) Rating Schema
# -------------------------------------------------------
class RatingSchema(Schema):
    reviewer_id: int
    reviewed_id: int
    rating: int  # Store rating as a percentage (0-100%)
    feedback: str = None
    created_at: datetime
