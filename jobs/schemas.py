from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
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

from ninja import Schema
from typing import Optional
from datetime import datetime, date, time

class JobDetailSchema(Schema):
    id: int
    title: str
    description: str
    status: str
    date: Optional[date]  # Job scheduled date
    start_time: Optional[time]
    end_time: Optional[time]
    duration: str  # Actual worked duration
    rate: str  # String to prevent floating point issues
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_shift_ongoing: bool
    employer_name: str  # Client's name
    date_posted: Optional[datetime]  # Job creation timestamp
    updated_at: Optional[datetime]  # Last update timestamp
    no_of_application: int  # Number of accepted applicants
    applicants_needed: int  # Total applicants required
    job_type: str  # single_day | multiple_days
    shift_type: str  # morning | afternoon | night
    payment_status: str  # pending, held, completed, etc.
    total_amount: str  # Total earnings
    service_fee: str  # Service fee deducted
    start_date: datetime # Redundant for clarity
    start_time_str: Optional[str]  # Start time as string
    end_time_str: Optional[str]  # End time as string



class CreateJobSchema(Schema):
    title: str
    industry: str  # Can be ID or name
    subcategory: str  # Can be ID or name
    applicants_needed: int
    job_type: str
    shift_type: str
    date: str  # Expected format: "YYYY-MM-DD"
    start_time: str  # Expected format: "HH:MM"
    end_time: str  # Expected format: "HH:MM"
    duration: str
    rate: float
    location: str
    payment_status: str

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
    """
    Full rating details, e.g. when returning rating objects to the frontend.
    """
    reviewer_id: int
    reviewed_id: int
    rating: float
    feedback: Optional[str] = None
    created_at: datetime

class RatingCreateSchema(Schema):
    """
    Incoming payload to create a new rating:
      {
        "reviewed_id": 123,
        "rating": 5,
        "feedback": "Optional text..."
      }
    """
    reviewed_id: int
    rating: Optional[float] = None
    feedback: Optional[str] = None


# -------------------------------------------------------
# 9) Profile Schema
# -------------------------------------------------------
class ProfileSchema(Schema):
    user: UserSchema
    phone_number: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    balance: int
    

class UpdateProfileSchema(Schema):
    phone_number: Optional[str] = None
    location: Optional[str] = None



class DisputeCreateSchema(BaseModel):
    """Schema for creating a dispute"""
    title: str
    description: str

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