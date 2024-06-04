"""
This module allows you to specify the database tables visible in the django admin page"""

from django.contrib import admin
from .models import Query
from .models import Eval
from .models import CustomUser
from .models import Team


# Register your models here.
admin.site.register(Query)
admin.site.register(Eval)
admin.site.register(CustomUser)
admin.site.register(Team)
