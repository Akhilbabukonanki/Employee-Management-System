# 🏢 Employee Management System

A production-quality, full-stack **Employee Management System** built with **Django 5**, **Bootstrap 5**, **Chart.js**, and **SQLite** (MySQL-ready). Developed as a college mini-project and portfolio showcase.

---

## 🚀 Features

- 🔐 **Authentication** — Admin login, logout, session auth, password hashing, login-required protection
- 📊 **Dashboard** — Live KPI cards, Chart.js (department, status, monthly trend) charts
- 👥 **Employee CRUD** — Add, View, Edit, Delete with custom auto-generated IDs (EMP0001...)
- 🔍 **Search & Filter** — By name, ID, email, phone, department, designation; filter by dept/status/salary/date
- 📄 **Sorting & Pagination** — Column-sortable table with 10 records per page
- 📤 **Export** — Export to CSV/Excel, Print-ready PDF (or browser print fallback)
- 🌙 **Dark Mode** — Toggle with localStorage persistence
- 📱 **Responsive** — Mobile-first Bootstrap 5 layout with collapsible sidebar
- 🖨️ **Print Profile** — Print-ready CSS for employee detail pages
- 🛡️ **Custom Admin** — Enhanced Django admin panel with search, filters, and fieldsets

---

## 🗂️ Project Structure

```
employee_management/
├── manage.py
├── requirements.txt
├── db.sqlite3               (auto-created after migrate)
│
├── employee_management/     (project config)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── employee/                (main app)
│   ├── models.py            (Employee model)
│   ├── views.py             (CBVs: Login, Dashboard, CRUD, Search, Exports)
│   ├── forms.py             (EmployeeForm with validation)
│   ├── urls.py              (URL routing)
│   ├── admin.py             (Customized admin panel)
│   └── templates/employee/
│       ├── base.html        (Sidebar layout + dark mode + messages)
│       ├── login.html
│       ├── dashboard.html   (KPI cards + 3 Chart.js charts)
│       ├── employee_list.html (Filters, sorting, pagination)
│       ├── employee_detail.html (Profile + print)
│       ├── add_employee.html (Form + image upload preview)
│       ├── edit_employee.html
│       ├── delete_confirm.html
│       ├── search.html
│       ├── pdf_fallback.html
│       ├── 404.html
│       └── 500.html
│
└── static/
    ├── css/styles.css       (Custom design system + dark mode)
    └── js/
        ├── main.js          (Sidebar, dark mode, image preview)
        └── charts.js        (Chart.js config)
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Install Dependencies
```bash
cd Employee_Management_System/employee_management
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```
Or use the pre-created account:
- **Username:** `admin`
- **Password:** `admin123`

### 5. Run the Server
```bash
python manage.py runserver
```
Open your browser at: **http://127.0.0.1:8000/**

---

## 🗄️ MySQL Configuration (Optional)

If you want to switch to MySQL instead of SQLite:

1. Install `mysqlclient`:
   ```bash
   pip install mysqlclient
   ```

2. Create the database in MySQL:
   ```sql
   CREATE DATABASE employee_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. In `employee_management/settings.py`, comment out the SQLite block and uncomment the MySQL block:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'employee_db',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

4. Re-run migrations:
   ```bash
   python manage.py migrate
   ```

---

## 🌐 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | Redirect | Redirects to `/dashboard/` |
| `/login/` | EmployeeLoginView | Login page |
| `/logout/` | EmployeeLogoutView | Logout |
| `/dashboard/` | DashboardView | Main dashboard |
| `/employees/` | EmployeeListView | Full directory table |
| `/employees/add/` | EmployeeCreateView | Add new employee |
| `/employees/<id>/` | EmployeeDetailView | View profile |
| `/employees/edit/<id>/` | EmployeeUpdateView | Edit profile |
| `/employees/delete/<id>/` | EmployeeDeleteView | Delete confirmation |
| `/employees/search/` | EmployeeSearchView | Search results |
| `/export/excel/` | ExportExcelView | Download CSV |
| `/export/pdf/` | ExportPDFView | Print/PDF report |
| `/admin/` | Django Admin | Admin panel |

---

## 🔧 Git Initialization & GitHub Upload

```bash
# Initialize Git repo
git init
git add .
git commit -m "feat: Initial Employee Management System - Django 5 + Bootstrap 5"

# Push to GitHub (replace with your repo URL)
git remote add origin https://github.com/yourusername/employee-management-system.git
git branch -M main
git push -u origin main
```

---

## 🔮 Future Improvements

- [ ] REST API with Django REST Framework
- [ ] Employee leave management module
- [ ] Attendance tracking with QR code
- [ ] Email notifications (joining / salary update)
- [ ] Department-specific roles and permissions
- [ ] Two-factor authentication
- [ ] Docker containerization for deployment

---

## 📝 License

Built for educational purposes. Free to use and modify.
