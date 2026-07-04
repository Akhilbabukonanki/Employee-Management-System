/* -----------------------------------------------------------------------------
   Employee Management System - Core JavaScript
----------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function() {
    
    // -------------------------------------------------------------------------
    // SIDEBAR TOGGLE
    // -------------------------------------------------------------------------
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('show');
            } else {
                sidebar.classList.toggle('collapsed');
            }
        });
    }
    
    // Close sidebar on mobile clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar && sidebarToggle) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target) && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        }
    });

    // -------------------------------------------------------------------------
    // DARK MODE TOGGLE
    // -------------------------------------------------------------------------
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Check local storage for preference
    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';
    if (isDarkMode) {
        body.classList.add('dark-mode');
        updateDarkModeIcon(true);
    }
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentMode = body.classList.contains('dark-mode');
            
            if (currentMode) {
                body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
                updateDarkModeIcon(false);
            } else {
                body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
                updateDarkModeIcon(true);
            }
        });
    }
    
    function updateDarkModeIcon(enabled) {
        const icon = darkModeToggle ? darkModeToggle.querySelector('i') : null;
        if (icon) {
            if (enabled) {
                icon.className = 'bi bi-sun-fill';
            } else {
                icon.className = 'bi bi-moon-fill';
            }
        }
    }

    // -------------------------------------------------------------------------
    // IMAGE UPLOAD PREVIEW
    // -------------------------------------------------------------------------
    const photoInput = document.getElementById('id_photo');
    const photoPreview = document.getElementById('photo-preview');
    
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // -------------------------------------------------------------------------
    // AUTO-CLOSE BOOTSTRAP ALERTS
    // -------------------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000); // 5 seconds
    });
});
