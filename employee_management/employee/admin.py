from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Custom Admin configuration for the Employee model.
    Includes list display, search, filters, and ordering.
    """
    list_display = ('id', 'name', 'department', 'designation', 'email', 'phone', 'salary', 'status', 'joining_date')
    list_filter = ('department', 'status', 'gender', 'joining_date')
    search_fields = ('id', 'name', 'email', 'phone', 'designation', 'department')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'joining_date'

    fieldsets = (
        ('Personal Information', {
            'fields': ('id', 'name', 'email', 'phone', 'gender', 'address', 'photo')
        }),
        ('Employment Details', {
            'fields': ('department', 'designation', 'salary', 'joining_date', 'status')
        }),
        ('System Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
