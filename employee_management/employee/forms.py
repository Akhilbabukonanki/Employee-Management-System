import re
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name', 'email', 'phone', 'department', 'designation', 
            'salary', 'gender', 'address', 'joining_date', 'status', 'photo'
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter street address, city, state, and ZIP code'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add form control styling classes
            if field_name in ['department', 'gender', 'status']:
                field.widget.attrs['class'] = 'form-select'
            elif field_name == 'photo':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Apply placeholder unless it's a date or select field
            if field_name not in ['joining_date', 'department', 'gender', 'status', 'photo']:
                field.widget.attrs['placeholder'] = f"Enter {field.label.lower()}"

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Allow numbers, spaces, dashes, parentheses and a leading plus, must be 10-15 digits
        pattern = re.compile(r'^\+?[0-9\s\-()]{10,15}$')
        if not pattern.match(phone):
            raise forms.ValidationError("Enter a valid phone number containing 10 to 15 digits.")
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError("Salary must be a positive number.")
        return salary

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Validate size (max 5 MB)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Profile photo size must be under 5MB.")
            # Validate file extension
            extension = photo.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'gif']:
                raise forms.ValidationError("Only JPG, JPEG, PNG, and GIF images are allowed.")
        return photo
