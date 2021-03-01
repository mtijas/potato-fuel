from django.contrib import admin

# Register your models here.
from .models import Car
from .models import Fill
from .models import Department

admin.site.register(Car)
admin.site.register(Fill)
admin.site.register(Department)