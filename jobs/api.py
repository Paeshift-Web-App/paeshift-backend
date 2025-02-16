from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from ninja import *
from ninja.responses import Response

from .models import *
from .router import *
from .schemas import *

from .auth import *
from .jobs import *
from .ratings import *

