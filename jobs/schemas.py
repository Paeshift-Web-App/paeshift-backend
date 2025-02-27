from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import Optional

# -------------------------------------------------------
# 1) Location Schema
# -------------------------------------------------------
class LocationSchema(Schema):
    latitude: float
    longitude: float


# -------------------------------------------------------
# 2) Authentication Schemas
# -------------------------------------------------------
class LoginSchema(Schema):
    email: str
    password: str

class SignupSchema(Schema):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    role: str


# -------------------------------------------------------
# 3) User Schema
# -------------------------------------------------------
class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    role : str


# -------------------------------------------------------
# 4) Job Schemas
# -------------------------------------------------------
class JobListSchema(Schema):
    id: int
    title: str
    description: Optional[str] = None
    client_name: str
    status: str
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[str] = None
    amount: Decimal = 0.0
    image: Optional[str] = None
    location: Optional[str] = None
    date_posted: str
    no_of_application: int

class JobDetailSchema(JobListSchema):
    applicant_name: Optional[str] = None
    payment_status: str


class CreateJobSchema(Schema):
    title: str
    industry: Optional[str] = None
    subcategory: Optional[str] = None
    applicants_needed: Optional[int] = 1
    job_type: Optional[str] = "single_day"
    shift_type: Optional[str] = "day_shift"
    date: str
    start_time: str
    end_time: str
    duration: Optional[str] = None
    rate: Optional[float] = None
    location: Optional[str] = None
    payment_status: Optional[str] = "Pending"

# -------------------------------------------------------
# 5) Application Schemas
# -------------------------------------------------------
class ApplicationListSchema(Schema):
    id: int
    job_id: int
    applicant_name: str
    is_accepted: bool
    applied_at: datetime

class CreateApplicationSchema(Schema):
    job_id: int


# -------------------------------------------------------
# 6) Saved Jobs Schema
# -------------------------------------------------------
class SavedJobSchema(Schema):
    id: int
    job_id: int
    title: str
    status: str
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[str] = None
    amount: Decimal = 0.0
    location: Optional[str] = None
    saved_at: datetime

class CreateSavedJobSchema(Schema):
    job_id: int


# -------------------------------------------------------
# 7) Payment Schemas
# -------------------------------------------------------
class PaymentSchema(Schema):
    job_id: int
    total: Decimal  # Amount before deduction

class PaymentDetailSchema(Schema):
    id: int
    payer_name: str
    recipient_name: Optional[str] = None
    original_amount: Decimal
    service_fee: Decimal
    final_amount: Decimal
    payment_status: str
    created_at: datetime


# -------------------------------------------------------
# 8) Rating Schema
# -------------------------------------------------------

class RatingSchema(Schema):
    reviewer_id: int
    reviewed_id: int
    rating: int  # Store rating as a percentage (0-100%)
    feedback: Optional[str] = None
    created_at: datetime

class RatingCreateSchema(Schema):
    reviewed_id: int
    rating: int
    feedback: Optional[str] = None



# -------------------------------------------------------
# 9) Profile Schema
# -------------------------------------------------------
class ProfileSchema(Schema):
    user: UserSchema
    phone_number: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime

class UpdateProfileSchema(Schema):
    phone_number: Optional[str] = None
    location: Optional[str] = None


class DisputeCreateSchema(Schema):
    user: UserSchema


class DisputeUpdateSchema(Schema):
    user: UserSchema
    

class PaymentCreateSchema(Schema):
    user: UserSchema
    

class PaymentCreateSchema(Schema):
    user: UserSchema
    
class PaymentUpdateSchema(Schema):
    user: UserSchema
  
  
class IndustrySchema(Schema):
    id: int
    name: str

class SubCategorySchema(Schema):
    id: int
    name: str
    industry_id: int  # or industry: IndustrySchema if you want nested detail