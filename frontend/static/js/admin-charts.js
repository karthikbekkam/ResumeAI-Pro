// Admin Panel Chart.js Analytics Integration

document.addEventListener('DOMContentLoaded', () => {
    const pieChartElem = document.getElementById('adminAtsPieChart');

    if (pieChartElem) {
        fetch('/admin/api/analytics')
            .then(res => res.json())
            .then(data => {
                if (data.ats_distribution) {
                    new Chart(pieChartElem, {
                        type: 'doughnut',
                        data: {
                            labels: ['0-40% (Poor)', '41-60% (Average)', '61-80% (Good)', '81-100% (Excellent)'],
                            datasets: [{
                                data: [
                                    data.ats_distribution['0-40'],
                                    data.ats_distribution['41-60'],
                                    data.ats_distribution['61-80'],
                                    data.ats_distribution['81-100']
                                ],
                                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                                borderWidth: 2,
                                borderColor: '#ffffff'
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'bottom'
                                }
                            },
                            cutout: '65%'
                        }
                    });
                }
            })
            .catch(err => console.error("Error loading admin charts:", err));
    }
});
