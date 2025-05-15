from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import time
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q, F
from decimal import Decimal

####################################################################


# Department Model
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class FaceEmbedding(models.Model):
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE, related_name="face_embeddings")
    embedding = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding {self.id} for {self.employe.name}"

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employe_profile")
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    face_embedding = models.JSONField(blank=True, null=True)
    authorized = models.BooleanField(default=False)
    emp_id = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    mother_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    department = models.ManyToManyField(Department, related_name="employes")

    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    per_day_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Salary per working day")

    def __str__(self):
        return self.name

    def calculate_salaries(self):
        # Ensure base_salary and allowances are Decimals
        total_salary = Decimal(self.base_salary) + Decimal(self.allowances)
        
        # Calculate the per day salary based on total salary and assuming 26 working days
        days_in_month = Decimal(26)  # Ensure days_in_month is a Decimal
        self.per_day_salary = total_salary / days_in_month

    def save(self, *args, **kwargs):
        # Calculate basic salary, allowances, and per day salary before saving
        self.calculate_salaries()

        # Call the parent class save method to save the employee instance
        super().save(*args, **kwargs)

    
#################################################################
from datetime import timedelta
class Attendance(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Absent')
    is_late = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    overtime_hours = models.FloatField(default=0.0)  # Overtime field

    def __str__(self):
        return f"{self.employe.name} - {self.date}"

    def mark_checked_in(self):
        self.check_in_time = timezone.now()
        self.status = 'Present'

        # Fetch the Employe's late check-in policy
        policy = self.employe.late_checkin_policy
        if policy:
            # Convert the late check-in time to the local timezone
            current_local_time = timezone.localtime()
            late_check_in_threshold = current_local_time.replace(
                hour=policy.start_time.hour,
                minute=policy.start_time.minute,
                second=0,
                microsecond=0
            )

            # Check if the check-in time is late
            if self.check_in_time > late_check_in_threshold:
                self.is_late = True

        self.save()

    def mark_checked_out(self):
        if self.check_in_time:
            self.check_out_time = timezone.now()
            self.save()  # Save after updating check-out time
        else:
            raise ValueError("Cannot mark check-out without check-in.")

    def calculate_duration(self):
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        return None

    def calculate_overtime(self):
        """Calculate overtime and update the overtime_hours field."""
        if self.check_in_time and self.check_out_time:
            stayed_duration = self.check_out_time - self.check_in_time
            stayed_hours = stayed_duration.total_seconds() / 3600  # Convert to hours
            overtime = max(stayed_hours - 4, 0) # 4 là số giờ làm việc bình thường
            return overtime
        return 0.0

    def save(self, *args, **kwargs):
        if not self.pk:  # Set the date only when creating a new record
            self.date = timezone.now().date()

        # Ensure overtime calculation before saving
        self.overtime_hours = self.calculate_overtime()
        super().save(*args, **kwargs)

#################################################

class Leave(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField(help_text="Leave start date")
    end_date = models.DateField(help_text="Leave end date")
    reason = models.TextField(help_text="Reason for the leave", blank=True, null=True)
    approved = models.BooleanField(default=False, help_text="Whether the leave has been approved")

    def __str__(self):
        return f"{self.employe.name} - {self.start_date} to {self.end_date} ({'Approved' if self.approved else 'Pending'})"


#############################################################
class Salary(models.Model):
    employee = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="salaries")
    month = models.IntegerField(help_text="Month (1-12)")
    year = models.IntegerField(help_text="Year")

    # Salary Components
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"), help_text="Overtime hours worked")
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="Performance or festival bonus")

    # Overtime Rate
    overtime_rate = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal("0.00"), help_text="Overtime rate per hour", editable=False)

    # Deductions
    tax_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="Income tax deductions")
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), help_text="Other deductions")
    # Absence Deduction (calculated based on per_day_salary)
    absence_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), editable=False)

    # Final Calculations
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), editable=False)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"), editable=False)

    def save(self, *args, **kwargs):
        # Fetch employee salary details
        self.base_salary = self.employee.base_salary
        self.allowances = self.employee.allowances

        # Constants (assumed)
        WORKING_DAYS_PER_MONTH = Decimal("26")  
        WORKING_HOURS_PER_DAY = Decimal("4")

        # Calculate hourly rate
        hourly_rate = self.base_salary / (WORKING_DAYS_PER_MONTH * WORKING_HOURS_PER_DAY)

        # Overtime Rate (1.5x of hourly rate)
        self.overtime_rate = hourly_rate * Decimal("1.5")

        # Fetch overtime hours from the Attendance model for the current month and year
        total_overtime_hours = Attendance.objects.filter(
            employe=self.employee,
            date__month=self.month,
            date__year=self.year,
            status="Present"
        ).aggregate(total_overtime=models.Sum('overtime_hours'))['total_overtime'] or Decimal("0.00")

        # Convert total_overtime_hours to Decimal if it's a float
        total_overtime_hours = Decimal(total_overtime_hours)

        # Save the total overtime hours in the model field
        self.overtime_hours = total_overtime_hours

        # Calculate Overtime Pay
        overtime_pay = total_overtime_hours * self.overtime_rate

        # Calculate the number of absent days without approved leave
        absences_without_leave = Attendance.objects.filter(
            employe=self.employee,
            date__month=self.month,
            date__year=self.year,
            status='Absent'
        ).exclude(
            Q(employe__leaves__start_date__lte=F('date')) & Q(employe__leaves__end_date__gte=F('date')) & Q(employe__leaves__approved=True)
        ).count()

        # Calculate Absence Deduction based on per_day_salary
        self.absence_deduction = absences_without_leave * self.employee.per_day_salary

        # Calculate Gross Salary
        self.gross_salary = self.base_salary + self.allowances + overtime_pay + self.bonus

        # Calculate Net Salary with deductions
        total_deductions = self.tax_deductions + self.other_deductions + self.absence_deduction
        self.net_salary = self.gross_salary - total_deductions

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year} - ${self.net_salary}"




        
    
######################################################################

# Checkout Policy for each employe
class Settings(models.Model):
    employe = models.OneToOneField('Employe', on_delete=models.CASCADE, related_name='settings', null=True, blank=True)  # Link to Employe
    check_out_time_threshold = models.IntegerField(default=60)  # Default 8 hours in seconds

    def __str__(self):
        return f"Settings (Employe: {self.employe.name if self.employe else 'Global'}, Check-out Time Threshold: {self.check_out_time_threshold} seconds)"

# Signal to create default Settings for each Employe
@receiver(post_save, sender=Employe)
def create_default_settings(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(employe=instance)  # Automatically create the Settings object for the new Employe

####################################################
# Late Check-In Policy Model
class LateCheckInPolicy(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, related_name="late_checkin_policy")

    def get_default_start_time():
        return time(8, 0)  # Default time as 8:00 AM

    start_time = models.TimeField(default=get_default_start_time)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.employe.name} - Late Check-In After {self.start_time}"

# Signal to create default LateCheckInPolicy for each Employe
@receiver(post_save, sender=Employe)
def create_late_checkin_policy(sender, instance, created, **kwargs):
    if created:
        LateCheckInPolicy.objects.create(employe=instance)
###################################################

class CameraConfiguration(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Give a name to this camera configuration")
    camera_source = models.CharField(max_length=255, help_text="Camera index (0 for default webcam or RTSP/HTTP URL for IP camera)")
    threshold = models.FloatField(default=0.6, help_text="Face recognition confidence threshold")
    location = models.CharField(max_length=255, null=True, default='Gate 1', help_text="Location of the camera (optional)")

    def __str__(self):
        return self.name

########################################################################
# Email Settings
class EmailConfig(models.Model):
    email_host = models.CharField(max_length=255)
    email_port = models.IntegerField()
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.CharField(max_length=255)
    email_host_password = models.CharField(max_length=255)

    def __str__(self):
        return f"Email Configuration for {self.email_host_user}"
    
###########################################################