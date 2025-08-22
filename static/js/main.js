// Main JavaScript file for Company Risk Analysis System

// Global variables
let currentData = null;
let currentAnalysis = null;

// Utility functions
const Utils = {
    // Format numbers with commas
    formatNumber: function(num) {
        if (num === null || num === undefined) return 'N/A';
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    // Format percentages
    formatPercentage: function(num) {
        if (num === null || num === undefined) return 'N/A';
        return num.toFixed(2) + '%';
    },
    
    // Format currency
    formatCurrency: function(num, currency = '€') {
        if (num === null || num === undefined) return 'N/A';
        return currency + ' ' + this.formatNumber(parseFloat(num).toFixed(2));
    },
    
    // Generate random color for charts
    getRandomColor: function() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },
    
    // Debounce function for performance
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },
    
    // Show loading spinner
    showLoading: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2 text-muted">Loading...</p>
                </div>
            `;
        }
    },
    
    // Hide loading spinner
    hideLoading: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '';
        }
    },
    
    // Show success message
    showSuccess: function(message, duration = 5000) {
        this.showMessage(message, 'success', duration);
    },
    
    // Show error message
    showError: function(message, duration = 5000) {
        this.showMessage(message, 'danger', duration);
    },
    
    // Show warning message
    showWarning: function(message, duration = 5000) {
        this.showMessage(message, 'warning', duration);
    },
    
    // Show info message
    showInfo: function(message, duration = 5000) {
        this.showMessage(message, 'info', duration);
    },
    
    // Generic message display function
    showMessage: function(message, type = 'info', duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    },
    
    // Validate file upload
    validateFile: function(file, allowedTypes = ['.xlsx', '.csv'], maxSize = 16 * 1024 * 1024) {
        const errors = [];
        
        // Check file type
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            errors.push(`File type ${fileExtension} is not supported. Allowed types: ${allowedTypes.join(', ')}`);
        }
        
        // Check file size
        if (file.size > maxSize) {
            const maxSizeMB = (maxSize / (1024 * 1024)).toFixed(1);
            errors.push(`File size (${(file.size / (1024 * 1024)).toFixed(1)}MB) exceeds maximum allowed size of ${maxSizeMB}MB`);
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    },
    
    // Download data as CSV
    downloadCSV: function(data, filename = 'export.csv') {
        if (!data || data.length === 0) {
            this.showError('No data to export');
            return;
        }
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => {
                const value = row[header];
                if (value === null || value === undefined) return '';
                return typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value;
            }).join(','))
        ].join('\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },
    
    // Create chart with consistent styling
    createChart: function(canvasId, type, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#007bff',
                    borderWidth: 1,
                    cornerRadius: 8
                }
            },
            elements: {
                point: {
                    radius: 4,
                    hoverRadius: 6
                }
            }
        };
        
        const finalOptions = this.mergeOptions(defaultOptions, options);
        
        return new Chart(ctx, {
            type: type,
            data: data,
            options: finalOptions
        });
    },
    
    // Merge options objects
    mergeOptions: function(defaultOptions, customOptions) {
        const merged = { ...defaultOptions };
        
        for (const key in customOptions) {
            if (customOptions.hasOwnProperty(key)) {
                if (typeof customOptions[key] === 'object' && !Array.isArray(customOptions[key])) {
                    merged[key] = this.mergeOptions(merged[key] || {}, customOptions[key]);
                } else {
                    merged[key] = customOptions[key];
                }
            }
        }
        
        return merged;
    },
    
    // Generate color palette for charts
    generateColorPalette: function(count) {
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384',
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'
        ];
        
        if (count <= colors.length) {
            return colors.slice(0, count);
        }
        
        // Generate additional colors if needed
        const additionalColors = [];
        for (let i = colors.length; i < count; i++) {
            additionalColors.push(this.getRandomColor());
        }
        
        return [...colors, ...additionalColors];
    }
};

// Data handling functions
const DataHandler = {
    // Parse CSV string to array of objects
    parseCSV: function(csvString) {
        const lines = csvString.split('\n');
        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
        const result = [];
        
        for (let i = 1; i < lines.length; i++) {
            if (lines[i].trim() === '') continue;
            
            const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
            const obj = {};
            
            headers.forEach((header, index) => {
                obj[header] = values[index] || '';
            });
            
            result.push(obj);
        }
        
        return result;
    },
    
    // Get unique values from array
    getUniqueValues: function(array, key) {
        return [...new Set(array.map(item => item[key]))];
    },
    
    // Filter data by multiple criteria
    filterData: function(data, filters) {
        return data.filter(item => {
            return Object.keys(filters).every(key => {
                const filterValue = filters[key];
                const itemValue = item[key];
                
                if (filterValue === null || filterValue === undefined || filterValue === '') {
                    return true;
                }
                
                if (typeof filterValue === 'string') {
                    return itemValue && itemValue.toString().toLowerCase().includes(filterValue.toLowerCase());
                }
                
                if (typeof filterValue === 'number') {
                    return itemValue === filterValue;
                }
                
                if (Array.isArray(filterValue)) {
                    return filterValue.includes(itemValue);
                }
                
                return itemValue === filterValue;
            });
        });
    },
    
    // Sort data by multiple keys
    sortData: function(data, sortKeys) {
        return data.sort((a, b) => {
            for (const sortKey of sortKeys) {
                const { key, direction = 'asc' } = sortKey;
                const aVal = a[key];
                const bVal = b[key];
                
                if (aVal === bVal) continue;
                
                let comparison = 0;
                if (aVal < bVal) comparison = -1;
                if (aVal > bVal) comparison = 1;
                
                return direction === 'desc' ? -comparison : comparison;
            }
            return 0;
        });
    }
};

// Chart utilities
const ChartUtils = {
    // Create bar chart
    createBarChart: function(canvasId, labels, data, options = {}) {
        const chartData = {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: Utils.generateColorPalette(data.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };
        
        const chartOptions = {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        };
        
        return Utils.createChart(canvasId, 'bar', chartData, this.mergeOptions(chartOptions, options));
    },
    
    // Create pie/doughnut chart
    createPieChart: function(canvasId, labels, data, type = 'doughnut', options = {}) {
        const chartData = {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: Utils.generateColorPalette(data.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        };
        
        return Utils.createChart(canvasId, type, chartData, options);
    },
    
    // Create line chart
    createLineChart: function(canvasId, labels, datasets, options = {}) {
        const chartData = {
            labels: labels,
            datasets: datasets.map((dataset, index) => ({
                ...dataset,
                borderColor: dataset.borderColor || Utils.getRandomColor(),
                backgroundColor: dataset.backgroundColor || Utils.getRandomColor() + '20',
                tension: 0.4
            }))
        };
        
        const chartOptions = {
            scales: {
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        };
        
        return Utils.createChart(canvasId, 'line', chartData, this.mergeOptions(chartOptions, options));
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
            }
        });
    });
});

// Export utilities for use in other scripts
window.Utils = Utils;
window.DataHandler = DataHandler;
window.ChartUtils = ChartUtils;
