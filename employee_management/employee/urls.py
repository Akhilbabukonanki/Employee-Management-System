from django.urls import path
from django.views.generic import RedirectView
from .views import (
    EmployeeLoginView, EmployeeLogoutView, DashboardView,
    EmployeeListView, EmployeeDetailView, EmployeeCreateView,
    EmployeeUpdateView, EmployeeDeleteView, EmployeeSearchView,
    ExportExcelView, ExportPDFView
)

urlpatterns = [
    # Redirect root to dashboard (which redirects to login if not authenticated)
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Authentication
    path('login/', EmployeeLoginView.as_view(), name='login'),
    path('logout/', EmployeeLogoutView.as_view(), name='logout'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Employee CRUD
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),

    # NOTE: specific named paths must come BEFORE the generic <str:pk>/ catch-all
    path('employees/search/', EmployeeSearchView.as_view(), name='employee_search'),

    path('employees/<str:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/edit/<str:pk>/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/delete/<str:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),

    # Exports
    path('export/excel/', ExportExcelView.as_view(), name='export_excel'),
    path('export/pdf/', ExportPDFView.as_view(), name='export_pdf'),
]
