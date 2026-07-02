import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q, Max, Avg, Count
from django.http import HttpResponse, Http404
from django.utils import timezone
from .models import Employee
from .forms import EmployeeForm

# -----------------------------------------------------------------------------
# AUTHENTICATION VIEWS
# -----------------------------------------------------------------------------

class EmployeeLoginView(LoginView):
    template_name = 'employee/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy('dashboard')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class EmployeeLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('login')

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('login')


# -----------------------------------------------------------------------------
# DASHBOARD VIEW
# -----------------------------------------------------------------------------

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        
        # Cards metrics
        total_employees = employees.count()
        active_employees = employees.filter(status='Active').count()
        inactive_employees = employees.filter(status='Inactive').count()
        departments_count = employees.values('department').distinct().count()
        
        highest_salary = employees.aggregate(Max('salary'))['salary__max'] or 0
        latest_joined = employees.order_by('-joining_date').first()
        recent_employees = employees.order_by('-created_at')[:5]

        # Charts data
        # 1. Employees by Department
        dept_counts = employees.values('department').annotate(count=Count('id'))
        dept_labels = [item['department'] for item in dept_counts]
        dept_values = [item['count'] for item in dept_counts]

        # 2. Employee Status
        status_counts = employees.values('status').annotate(count=Count('id'))
        status_labels = [item['status'] for item in status_counts]
        status_values = [item['count'] for item in status_counts]

        # 3. Monthly Joined (last 6 months, database-agnostic)
        monthly_labels = []
        monthly_values = []
        today = timezone.now().date()
        for i in range(5, -1, -1):
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
            month_name = datetime(year, month, 1).strftime('%b %Y')
            monthly_labels.append(month_name)
            
            count = employees.filter(
                joining_date__year=year,
                joining_date__month=month
            ).count()
            monthly_values.append(count)

        import json
        context = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'departments_count': departments_count,
            'highest_salary': highest_salary,
            'latest_joined': latest_joined,
            'recent_employees': recent_employees,
            'dept_labels_json': json.dumps(dept_labels),
            'dept_values_json': json.dumps(dept_values),
            'status_labels_json': json.dumps(status_labels),
            'status_values_json': json.dumps(status_values),
            'monthly_labels_json': json.dumps(monthly_labels),
            'monthly_values_json': json.dumps(monthly_values),
        }
        return render(request, 'employee/dashboard.html', context)


# -----------------------------------------------------------------------------
# EMPLOYEE CRUD VIEWS
# -----------------------------------------------------------------------------

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = Employee.objects.all()

        # Apply Filters
        dept = self.request.GET.get('department')
        status = self.request.GET.get('status')
        min_salary = self.request.GET.get('min_salary')
        max_salary = self.request.GET.get('max_salary')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if dept:
            queryset = queryset.filter(department=dept)
        if status:
            queryset = queryset.filter(status=status)
        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)
        if start_date:
            queryset = queryset.filter(joining_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(joining_date__lte=end_date)

        # Apply Sorting
        sort_by = self.request.GET.get('sort', 'name') # Default sort by name
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'desc':
            sort_by = '-' + sort_by
        
        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass filter choices to context
        context['departments'] = Employee.DEPARTMENT_CHOICES
        context['statuses'] = Employee.STATUS_CHOICES
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['current_direction'] = self.request.GET.get('direction', 'asc')
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/add_employee.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        messages.success(self.request, "Employee added successfully.")
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/edit_employee.html'
    
    def get_success_url(self):
        messages.success(self.request, "Employee details updated successfully.")
        return reverse_lazy('employee_detail', kwargs={'pk': self.object.pk})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete_confirm.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Employee has been deleted.")
        return super().delete(request, *args, **kwargs)


# -----------------------------------------------------------------------------
# SEARCH VIEW
# -----------------------------------------------------------------------------

class EmployeeSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        results = Employee.objects.all()
        
        if query:
            results = results.filter(
                Q(id__icontains=query) |
                Q(name__icontains=query) |
                Q(department__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(designation__icontains=query)
            )

        context = {
            'query': query,
            'employees': results,
            'results_count': results.count()
        }
        return render(request, 'employee/search.html', context)


# -----------------------------------------------------------------------------
# EXPORT VIEWS
# -----------------------------------------------------------------------------

class ExportExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="employees_{timestamp}.csv"'
        
        writer = csv.writer(response)
        # Header row
        writer.writerow([
            'Employee ID', 'Full Name', 'Email', 'Phone', 'Department', 
            'Designation', 'Salary', 'Gender', 'Address', 'Joining Date', 'Status'
        ])
        
        # Data rows
        employees = Employee.objects.all()
        for emp in employees:
            writer.writerow([
                emp.id, emp.name, emp.email, emp.phone, emp.get_department_display(),
                emp.designation, emp.salary, emp.gender, emp.address,
                emp.joining_date, emp.status
            ])
            
        return response


class ExportPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            
            response = HttpResponse(content_type='application/pdf')
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            response['Content-Disposition'] = f'attachment; filename="employee_list_{timestamp}.pdf"'
            
            doc = SimpleDocTemplate(
                response, 
                pagesize=letter, 
                rightMargin=30, 
                leftMargin=30, 
                topMargin=30, 
                bottomMargin=30
            )
            elements = []
            
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=22,
                spaceAfter=15,
                textColor=colors.HexColor('#0f172a') # Deep Slate
            )
            
            elements.append(Paragraph("Employee Management System - Employee List", title_style))
            elements.append(Spacer(1, 10))
            
            # Build Table Headers
            data = [['ID', 'Name', 'Email', 'Department', 'Designation', 'Status']]
            for emp in Employee.objects.all():
                data.append([
                    emp.id, 
                    emp.name, 
                    emp.email, 
                    emp.get_department_display(), 
                    emp.designation, 
                    emp.status
                ])
                
            t = Table(data, colWidths=[70, 100, 140, 90, 90, 60])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')), # Navy Blue
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')]),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            elements.append(t)
            doc.build(elements)
            return response
            
        except ImportError:
            # Fallback to printable HTML report
            employees = Employee.objects.all()
            return render(request, 'employee/pdf_fallback.html', {'employees': employees})

def custom_404_view(request, exception=None):
    return render(request, 'employee/404.html', status=404)

def custom_500_view(request):
    return render(request, 'employee/500.html', status=500)
