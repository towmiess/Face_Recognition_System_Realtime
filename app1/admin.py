from django.contrib import admin
from .models import (
    Settings, Employe, Department, 
    LateCheckInPolicy, Attendance, CameraConfiguration, 
    EmailConfig, Leave,FaceEmbedding,Salary
)

# ---------------- Department Model Admin ----------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


# ---------------- Employe Model Admin ----------------
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('name', 'emp_id', 'email', 'phone_number', 'authorized')
    search_fields = ('name', 'emp_id', 'email')
    list_filter = ('authorized',)
    ordering = ('name',)


# ---------------- Late Check-In Policy Admin ----------------
@admin.register(LateCheckInPolicy)
class LateCheckInPolicyAdmin(admin.ModelAdmin):
    list_display = ('employe_name', 'start_time', 'description')
    search_fields = ('employe__name',)
    ordering = ('-start_time',)

    def employe_name(self, obj):
        return obj.employe.name if obj.employe else "N/A"
    employe_name.short_description = 'Employe'


# ---------------- Attendance Model Admin ----------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employe_name', 'date', 'check_in_time', 'check_out_time', 'status', 'is_late')
    search_fields = ('employe__name', 'date')
    list_filter = ('status', 'is_late', 'date')
    ordering = ('-date',)

    def employe_name(self, obj):
        return obj.employe.name if obj.employe else "N/A"
    employe_name.short_description = 'Employe'


# ---------------- Camera Configuration Admin ----------------
@admin.register(CameraConfiguration)
class CameraConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'camera_source', 'threshold')
    search_fields = ('name', 'camera_source')
    ordering = ('name',)


# ---------------- Email Configuration Admin ----------------
@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    list_display = ('email_host', 'email_port', 'email_use_tls', 'email_host_user')
    search_fields = ('email_host', 'email_host_user')
    list_filter = ('email_use_tls',)
    ordering = ('email_host',)


# ---------------- Global & Employee-Specific Settings Admin ----------------
@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'employe_name', 'check_out_time_threshold', 'is_global_setting')
    list_filter = ('employe',)
    search_fields = ('employe__name',)
    ordering = ('-id',)

    def employe_name(self, obj):
        return obj.employe.name if obj.employe else 'Global'
    employe_name.short_description = 'Employe Name'

    def is_global_setting(self, obj):
        return obj.employe is None
    is_global_setting.short_description = 'Global Setting'
    is_global_setting.boolean = True


# ---------------- Leave Management Admin ----------------
@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employe_name', 'start_date', 'end_date', 'approved', 'reason')
    list_filter = ('approved', 'start_date')
    search_fields = ('employe__name', 'reason')
    ordering = ('-start_date',)

    def employe_name(self, obj):
        return obj.employe.name if obj.employe else "N/A"
    employe_name.short_description = 'Employe'


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("employee", "month", "year", "base_salary", "allowances","absence_deduction", "overtime_hours", "bonus", "gross_salary", "net_salary")
    list_filter = ("month", "year", "employee")
    search_fields = ("employee__name", "month", "year")
    
    readonly_fields = ("gross_salary", "net_salary", "overtime_rate")  # Make computed fields read-only
    exclude = ("overtime_rate",)  # Prevent the error by excluding non-editable fields


@admin.register(FaceEmbedding)
class FaceEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'employe', 'created_at')
    search_fields = ('employe__name',)
    list_filter = ('created_at',)