// User Dashboard Chart.js Integration

document.addEventListener('DOMContentLoaded', () => {
    const atsChartElem = document.getElementById('atsTrendChart');
    const jobChartElem = document.getElementById('jobMatchChart');

    if (atsChartElem || jobChartElem) {
        fetch('/dashboard/api/chart-data')
            .then(res => res.json())
            .then(data => {
                // 1. ATS Score Progress Chart
                if (atsChartElem && data.ats_trend) {
                    new Chart(atsChartElem, {
                        type: 'line',
                        data: {
                            labels: data.ats_trend.labels,
                            datasets: [{
                                label: 'ATS Score (%)',
                                data: data.ats_trend.scores,
                                borderColor: '#6366f1',
                                backgroundColor: 'rgba(99, 102, 241, 0.15)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.3,
                                pointBackgroundColor: '#4f46e5',
                                pointRadius: 5
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    min: 0,
                                    max: 100,
                                    grid: { color: '#f1f5f9' }
                                },
                                x: {
                                    grid: { display: false }
                                }
                            }
                        }
                    });
                }

                // 2. Job Match Bar Chart
                if (jobChartElem && data.job_match_trend) {
                    new Chart(jobChartElem, {
                        type: 'bar',
                        data: {
                            labels: data.job_match_trend.labels,
                            datasets: [{
                                label: 'Match %',
                                data: data.job_match_trend.scores,
                                backgroundColor: [
                                    '#10b981', '#6366f1', '#ec4899', '#f59e0b', '#3b82f6'
                                ],
                                borderRadius: 8
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    min: 0,
                                    max: 100,
                                    grid: { color: '#f1f5f9' }
                                },
                                x: {
                                    grid: { display: false }
                                }
                            }
                        }
                    });
                }
            })
            .catch(err => console.error("Error loading dashboard charts:", err));
    }
});
