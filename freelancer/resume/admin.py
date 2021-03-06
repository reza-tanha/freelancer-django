from django.contrib import admin

from .models import CV, Contact, Education, WorkExperience


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "gender", "marital_status")    
    list_display_links = ("user",)
    list_filter = ("gender", "marital_status")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("cv","image", "link")    
    list_filter = ("cv","image", "link")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("cv","evidence", "location", "start_year", "end_year")    
    list_filter = ("cv","evidence", "location", "start_year", "end_year")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("cv","position", "location", "start_year", "end_year")    
    list_filter = ("cv","position", "location", "start_year", "end_year")