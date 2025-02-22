from ninja import Schema
from datetime import datetime
from decimal import Decimal
from typing import Optional

# ------------------------------------------------------
# SCHEMAS
# ------------------------------------------------------
class EmailSignupSchema(Schema):
    """Used for email/password signup."""
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str

class EmailLoginSchema(Schema):
    """Used for email/password login."""
    email: str
    password: str

class SocialLoginSchema(Schema):
    """
    Generic schema for social logins.
    The front-end would pass:
      provider: "google" or "facebook" or "apple"
      access_token: The token from the front-end's social login
    """
    provider: str
    access_token: str
