from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)

"""
    This `admin registration` is done to show the table/class which we created in models.py at `django administration` page.
Otherwise it doesn't show in `django administration` page.   
"""