let forecastChart = null;

document.addEventListener("DOMContentLoaded", function () {
    const loadBtn = document.getElementById("loadForecastBtn");
    const streetFilter = document.getElementById("streetFilter");
    
    loadBtn.addEventListener("click", loadForecast);
    
    // Load forecast if street is pre-selected
    if (streetFilter.value) {
        loadForecast();
    }
});

async function loadForecast() {
    const streetId = document.getElementById("streetFilter").value;
    const loadingMsg = document.getElementById("loadingMessage");
    const chartContainer = document.getElementById("chartContainer");
    
    loadingMsg.textContent = "Loading prediction...";
    loadingMsg.style.display = "block";
    chartContainer.style.display = "none";
    
    try {
        const url = `/admin/api/forecast?street_id=${streetId}&history_days=30&forecast_days=1`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            loadingMsg.textContent = "Error: " + data.error;
            loadingMsg.style.color = "#dc2626";
            return;
        }
        
        // Check if there's data
        if (!data.historical || data.historical.length === 0) {
            loadingMsg.textContent = "No historical data available for this street. Please run predictions first.";
            loadingMsg.style.color = "#f59e0b";
            return;
        }
        
        // Update statistics
        updateStatistics(data.statistics);
        
        // Create/update chart
        createForecastChart(data);
        
        // Update forecast table
        updateForecastTable(data.forecast);
        
        loadingMsg.style.display = "none";
        chartContainer.style.display = "block";
        
    } catch (error) {
        console.error("Error loading forecast:", error);
        loadingMsg.textContent = "Failed to load forecast. Please try again.";
        loadingMsg.style.color = "#dc2626";
        loadingMsg.style.display = "block";
    }
}

function updateStatistics(stats) {
    if (!stats) {
        stats = {mean: 0, max: 0, min: 0, trend: 'insufficient_data'};
    }
    
    document.getElementById("statMean").textContent = (stats.mean || 0).toFixed(3);
    document.getElementById("statMax").textContent = (stats.max || 0).toFixed(3);
    document.getElementById("statMin").textContent = (stats.min || 0).toFixed(3);
    
    const trendEl = document.getElementById("statTrend");
    const trendText = (stats.trend || 'unknown').replace('_', ' ').toUpperCase();
    trendEl.textContent = trendText;
    
    // Color code trend
    if (stats.trend === 'increasing') {
        trendEl.style.color = '#dc2626';
    } else if (stats.trend === 'decreasing') {
        trendEl.style.color = '#10b981';
    } else {
        trendEl.style.color = '#6b7280';
    }
}

function createForecastChart(data) {
    const ctx = document.getElementById("forecastChart").getContext("2d");
    
    // Prepare data
    const historical = data.historical || [];
    const forecast = data.forecast || [];
    
    const historicalLabels = historical.map(d => new Date(d.timestamp).toLocaleDateString());
    const historicalValues = historical.map(d => d.water_level);
    
    const forecastLabels = forecast.map(d => new Date(d.timestamp).toLocaleDateString());
    const forecastValues = forecast.map(d => d.water_level);
    
    // Combine labels
    const allLabels = [...historicalLabels, ...forecastLabels];
    
    // Connect forecast to last historical point
    const lastHistoricalValue = historicalValues.length > 0 ? historicalValues[historicalValues.length - 1] : null;
    const connectedForecastData = [...Array(historical.length - 1).fill(null), lastHistoricalValue, ...forecastValues];
    
    // Destroy existing chart
    if (forecastChart) {
        forecastChart.destroy();
    }
    
    // Create new chart
    forecastChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: [
                {
                    label: 'Historical Water Level',
                    data: [...historicalValues, ...Array(forecast.length).fill(null)],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Predicted Water Level',
                    data: connectedForecastData,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Water Level Forecast (Next 7 Days)',
                    font: { size: 16 }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1.0,
                    title: {
                        display: true,
                        text: 'Water Level (0-1.0)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

function updateForecastTable(forecast) {
    const container = document.getElementById("forecastTable");
    
    if (!forecast || forecast.length === 0) {
        container.innerHTML = '<p class="empty-message">No forecast data available</p>';
        return;
    }
    
    let html = '<table class="forecast-table">';
    html += '<thead><tr>';
    html += '<th>Date</th>';
    html += '<th>Water Level</th>';
    html += '<th>Severity</th>';
    html += '</tr></thead>';
    html += '<tbody>';
    
    forecast.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
        
        html += '<tr>';
        html += `<td>${date}</td>`;
        html += `<td><strong>${item.water_level.toFixed(3)}</strong></td>`;
        html += `<td><span class="severity-badge ${item.severity}">${item.severity.toUpperCase()}</span></td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}
