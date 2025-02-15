from ninja import Schema
from datetime import datetime
from typing import Optional

class LoginSchema(Schema):
    email: str
    password: str

class SignupSchema(Schema):
    firstName: str
    lastName: str
    email: str
    password: str
    confirmPassword: str
    
class JobSchema(Schema):
    id: int
    title: str
    description: str
    client_id: int
    created_at: datetime

class JobCreateSchema(Schema):
    title: str
    description: str

class ApplicationSchema(Schema):
    id: int
    job_id: int
    applicant_id: int
    is_accepted: bool

class LiveLocationSchema(Schema):
    latitude: float
    longitude: float
    job_id: int
    timestamp: datetime
