document.addEventListener("DOMContentLoaded", function () {
    const runPredictionBtn = document.getElementById("runPredictionBtn");

    if (!runPredictionBtn) return;

    const resultBox = document.getElementById("predictionResult");
    const waterLevelText = document.getElementById("waterLevelText");
    const severityText = document.getElementById("severityText");
    const confidenceText = document.getElementById("confidenceText");

    // Video ID comes from template (Flask session)
    const videoId = runPredictionBtn.dataset.videoId;

    // Key for localStorage
    const STORAGE_KEY = `prediction_${videoId}`;

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
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                runPredictionBtn.disabled = false;
                runPredictionBtn.innerText = "Run Prediction";
                return;
            }

            //  Save prediction persistently
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));

            // Update UI
            showPrediction(data);

            runPredictionBtn.disabled = false;
            runPredictionBtn.innerText = "Run Prediction";
        })
        .catch(err => {
            alert("Prediction failed. Check backend.");
            runPredictionBtn.disabled = false;
            runPredictionBtn.innerText = "Run Prediction";
            console.error(err);
        });
    });

    // Helper function: update UI
    function showPrediction(data) {
        resultBox.classList.remove("hidden");
        waterLevelText.textContent = data.water_level;
        confidenceText.textContent = data.confidence || "Coming soon";

        // Severity color coding
        severityText.textContent = data.severity.toUpperCase();
        severityText.className = "severity-tag";
        if (data.severity === "normal") severityText.classList.add("severity-normal");
        if (data.severity === "alert") severityText.classList.add("severity-alert");
        if (data.severity === "severe") severityText.classList.add("severity-severe");
    }
});
