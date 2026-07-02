/* -----------------------------------------------------------------------------
   Employee Management System - Dashboard Charts Config
----------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function() {
    
    // Custom Color Palette for Charts (Matches styles.css theme)
    const primaryColor = '#4f46e5';     // Indigo
    const successColor = '#10b981';     // Emerald
    const dangerColor = '#ef4444';      // Rose
    const warningColor = '#f59e0b';     // Amber
    const infoColor = '#06b6d4';        // Cyan
    
    const chartColors = [primaryColor, successColor, infoColor, warningColor, dangerColor, '#8b5cf6', '#ec4899'];
    const textSecondary = '#64748b';

    // -------------------------------------------------------------------------
    // 1. DEPARTMENT DISTRIBUTION CHART (DOUGHNUT)
    // -------------------------------------------------------------------------
    const deptCanvas = document.getElementById('deptChart');
    if (deptCanvas) {
        try {
            const labels = JSON.parse(deptCanvas.getAttribute('data-labels') || '[]');
            const values = JSON.parse(deptCanvas.getAttribute('data-values') || '[]');
            
            new Chart(deptCanvas, {
                type: 'doughnut',
                data: {
                    labels: labels.length ? labels : ['No Data'],
                    datasets: [{
                        data: values.length ? values : [0],
                        backgroundColor: labels.length ? chartColors.slice(0, labels.length) : ['#e2e8f0'],
                        borderWidth: 2,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: textSecondary,
                                font: { family: 'Inter', size: 12 }
                            }
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error drawing department chart: ", e);
        }
    }

    // -------------------------------------------------------------------------
    // 2. EMPLOYEE STATUS CHART (PIE)
    // -------------------------------------------------------------------------
    const statusCanvas = document.getElementById('statusChart');
    if (statusCanvas) {
        try {
            const labels = JSON.parse(statusCanvas.getAttribute('data-labels') || '[]');
            const values = JSON.parse(statusCanvas.getAttribute('data-values') || '[]');
            
            const statusBgColors = labels.map(label => {
                if (label.toLowerCase() === 'active') return successColor;
                if (label.toLowerCase() === 'inactive') return dangerColor;
                return primaryColor;
            });

            new Chart(statusCanvas, {
                type: 'pie',
                data: {
                    labels: labels.length ? labels : ['No Data'],
                    datasets: [{
                        data: values.length ? values : [0],
                        backgroundColor: labels.length ? statusBgColors : ['#e2e8f0'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: textSecondary,
                                font: { family: 'Inter', size: 12 }
                            }
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error drawing status chart: ", e);
        }
    }

    // -------------------------------------------------------------------------
    // 3. MONTHLY JOINED EMPLOYEES CHART (BAR/LINE MIX)
    // -------------------------------------------------------------------------
    const monthlyCanvas = document.getElementById('monthlyChart');
    if (monthlyCanvas) {
        try {
            const labels = JSON.parse(monthlyCanvas.getAttribute('data-labels') || '[]');
            const values = JSON.parse(monthlyCanvas.getAttribute('data-values') || '[]');
            
            new Chart(monthlyCanvas, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Joined Employees',
                        data: values,
                        fill: true,
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        borderColor: primaryColor,
                        tension: 0.3,
                        borderWidth: 3,
                        pointBackgroundColor: primaryColor,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: {
                                color: textSecondary,
                                font: { family: 'Inter', size: 11 }
                            }
                        },
                        y: {
                            grid: { color: 'rgba(226, 232, 240, 0.5)' },
                            ticks: {
                                color: textSecondary,
                                font: { family: 'Inter', size: 11 },
                                precision: 0
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error drawing monthly joining chart: ", e);
        }
    }
});
