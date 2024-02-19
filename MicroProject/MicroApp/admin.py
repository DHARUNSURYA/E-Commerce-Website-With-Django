from django.contrib import admin

# Register your models here.
from .models import *
#class CategoryAdmin(admin.ModelAdmin):
    #list_display=('name','image','description')
admin.site.register(Category)
admin.site.register(Product)