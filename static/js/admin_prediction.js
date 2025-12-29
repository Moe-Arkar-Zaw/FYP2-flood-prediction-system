let recentPredictionsChart = null;

document.addEventListener("DOMContentLoaded", function () {
    const runPredictionBtn = document.getElementById("runPredictionBtn");

    if (!runPredictionBtn) return;

    const resultBox = document.getElementById("predictionResult");
    const waterLevelText = document.getElementById("waterLevelText");
    const severityText = document.getElementById("severityText");

    // Video ID comes from template (Flask session)
    const videoId = runPredictionBtn.dataset.videoId;

    // Key for localStorage
    const STORAGE_KEY = `prediction_${videoId}`;

    // Load recent predictions on page load
    loadRecentPredictions();

    // Restore previous prediction if exists
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        const data = JSON.parse(saved);
        showPrediction(data); // restore UI
    }

    // Disable button if no video
    if (!videoId) {
        runPredictionBtn.disabled = true;
        runPredictionBtn.title = "Upload a video first";
        return;
    }

    runPredictionBtn.addEventListener("click", function () {
        runPredictionBtn.disabled = true;
        runPredictionBtn.innerText = "Running...";

        fetch("/admin/run_prediction", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ video_id: videoId })
        })
        .then(res => {
            // Check if response is ok
            if (!res.ok) {
                return res.json().then(err => Promise.reject(err));
            }
            return res.json();
        })
        .then(data => {
            console.log("Prediction response:", data);
            
            if (data.error) {
                alert("Prediction error: " + data.error);
                runPredictionBtn.disabled = false;
                runPredictionBtn.innerText = "Run Prediction";
                return;
            }

            //  Save prediction persistently
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));

            // Update UI
            showPrediction(data);
            
            // Reload recent predictions
            loadRecentPredictions();

            runPredictionBtn.disabled = false;
            runPredictionBtn.innerText = "Run Prediction";
        })
        .catch(err => {
            console.error("Prediction error:", err);
            alert("Prediction failed: " + (err.error || err.message || "Unknown error"));
            runPredictionBtn.disabled = false;
            runPredictionBtn.innerText = "Run Prediction";
        });
    });

    // Helper function: update UI
    function showPrediction(data) {
        resultBox.classList.remove("hidden");
        
        // Format water level to 3 decimal places
        const waterLevel = parseFloat(data.water_level).toFixed(3);
        waterLevelText.textContent = waterLevel;
        
        // Update video ID if available
        const videoIdEl = document.getElementById("videoIdText");
        if (videoIdEl && data.video_id) {
            videoIdEl.textContent = data.video_id;
        }
        
        // Update prediction time
        const timeEl = document.getElementById("predictionTimeText");
        if (timeEl) {
            timeEl.textContent = new Date().toLocaleString();
        }

        // Severity color coding
        const severity = data.severity.toUpperCase();
        severityText.textContent = severity;
        severityText.className = "severity-tag";
        if (data.severity === "normal") severityText.classList.add("severity-normal");
        if (data.severity === "alert") severityText.classList.add("severity-alert");
        if (data.severity === "severe") severityText.classList.add("severity-severe");
    }
    
    // Load recent predictions from API
    function loadRecentPredictions() {
        fetch("/api/predictions?limit=5")
            .then(res => res.json())
            .then(predictions => {
                const container = document.getElementById("recentPredictions");
                const statsBox = document.getElementById("averageStats");
                
                if (!predictions || predictions.length === 0) {
                    container.innerHTML = "<p>No predictions yet.</p>";
                    return;
                }
                
                // Create chart
                createRecentPredictionsChart(predictions);
                
                // Display predictions
                let html = "";
                predictions.forEach(pred => {
                    const date = new Date(pred.prediction_time).toLocaleString();
                    html += `
                        <div class="prediction-row ${pred.severity}">
                            <div>
                                <strong>${pred.severity.toUpperCase()}</strong>
                                <small style="display:block; color:#6b7280;">${pred.street_name || 'Street #' + pred.street_id}</small>
                                <small style="display:block; color:#9ca3af; font-size:11px;">${date}</small>
                            </div>
                            <div style="text-align:right;">
                                <strong style="font-size:18px;">${parseFloat(pred.water_level).toFixed(3)}</strong>
                                <small style="display:block; color:#6b7280;">Water Level</small>
                            </div>
                        </div>
                    `;
                });
                container.innerHTML = html;
                
                // Calculate average
                const avgLevel = predictions.reduce((sum, p) => sum + parseFloat(p.water_level), 0) / predictions.length;
                const severityCounts = {};
                predictions.forEach(p => {
                    severityCounts[p.severity] = (severityCounts[p.severity] || 0) + 1;
                });
                const mostCommon = Object.keys(severityCounts).reduce((a, b) => 
                    severityCounts[a] > severityCounts[b] ? a : b
                );
                
                document.getElementById("avgWaterLevel").textContent = avgLevel.toFixed(3);
                document.getElementById("commonSeverity").textContent = mostCommon.toUpperCase();
                statsBox.classList.remove("hidden");
            })
            .catch(err => {
                console.error("Error loading recent predictions:", err);
                document.getElementById("recentPredictions").innerHTML = 
                    "<p>Could not load recent predictions.</p>";
            });
    }
    
    // Create chart for recent predictions
    function createRecentPredictionsChart(predictions) {
        const ctx = document.getElementById("recentPredictionsChart");
        if (!ctx) return;
        
        // Reverse to show oldest to newest
        const sortedPredictions = [...predictions].reverse();
        
        // Prepare data with street names
        const labels = sortedPredictions.map(p => {
            const date = new Date(p.prediction_time);
            const timeStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const streetName = p.street_name || `Street #${p.street_id}`;
            return [streetName, timeStr];  // Multi-line label
        });
        
        const waterLevels = sortedPredictions.map(p => parseFloat(p.water_level));
        
        // Color points based on severity
        const pointColors = sortedPredictions.map(p => {
            if (p.severity === 'severe') return '#dc2626';
            if (p.severity === 'alert') return '#f59e0b';
            return '#10b981';
        });
        
        // Destroy existing chart
        if (recentPredictionsChart) {
            recentPredictionsChart.destroy();
        }
        
        // Create new chart
        recentPredictionsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Water Level',
                    data: waterLevels,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    pointBackgroundColor: pointColors,
                    pointBorderColor: pointColors,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Recent Predictions Timeline',
                        font: { size: 16 }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const pred = sortedPredictions[context.dataIndex];
                                return [
                                    `Water Level: ${pred.water_level}`,
                                    `Severity: ${pred.severity.toUpperCase()}`,
                                    `Street: ${pred.street_name || 'Street #' + pred.street_id}`
                                ];
                            }
                        }
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
                            text: 'Prediction Time'
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
});
