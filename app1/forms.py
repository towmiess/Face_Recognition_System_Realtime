from django import forms
from .models import LateCheckInPolicy
from django.core.exceptions import ValidationError
from django import forms
from django import forms
from .models import Employe
from django import forms
from .models import Employe
import json
from django import forms
from .models import Leave

class LateCheckInPolicyForm(forms.ModelForm):
    class Meta:
        model = LateCheckInPolicy
        fields = ['employe', 'start_time', 'description']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        employe = cleaned_data.get('employe')
        policy_id = self.instance.id  # Get the current instance's ID

        # Check if a LateCheckInPolicy already exists for this employe, excluding the current instance
        if employe and LateCheckInPolicy.objects.filter(employe=employe).exclude(id=policy_id).exists():
            raise ValidationError(f"A late check-in policy already exists for {employe.name}.")
        
        return cleaned_data

##################################################################

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
#######################################################################

from django import forms
from .models import Salary, Employe  # Assuming you have an Employee model

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'month', 'year', 'bonus', 'tax_deductions', 'other_deductions']
    
    # Make employee a selectable field (dropdown list)
    employee = forms.ModelChoiceField(queryset=Employe.objects.all(), required=True, label='Employee')
