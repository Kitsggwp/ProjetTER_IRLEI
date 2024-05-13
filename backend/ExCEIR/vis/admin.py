from django.contrib import admin
from .models import Query
from .models import Eval



# Register your models here.
admin.site.register(Query)
admin.site.register(Eval)