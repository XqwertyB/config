from django.contrib import admin
from .models import (
    Announcement,
    Category,
    Costumer,
    Organization,
    CompanyContact,
)

@admin.register(Announcement)
class Announcement_Admin(admin.ModelAdmin):
    list_display = ['title', 'sub_category_id', 'organization_id', ]

@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    pass


@admin.register(Costumer)
class Costumer_Admin(admin.ModelAdmin):
    list_display = ['name',  'phone']

@admin.register(Organization)
class Organization_Admin(admin.ModelAdmin):
    pass

@admin.register(CompanyContact)
class CompanyContact_Admin(admin.ModelAdmin):
    pass