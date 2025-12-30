document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("alertModal");
    const alertMessage = document.getElementById("alertMessage");

    const sendBtn = document.getElementById("sendAlertBtn");
    const closeBtn = document.getElementById("closeModalBtn");

    let selectedPredictionId = null;
    let selectedAlertType = null;
    let selectedStreetId = null;
    let selectedWaterLevel = null;

    // Open modal
    document.querySelectorAll(".publish-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            selectedAlertType = this.dataset.alertType;
            
            if (selectedAlertType === "estimation") {
                selectedPredictionId = this.dataset.predictionId;
            } else if (selectedAlertType === "prediction") {
                selectedStreetId = this.dataset.streetId;
                selectedWaterLevel = this.dataset.waterLevel;
            }
            
            alertMessage.value = "";
            modal.classList.remove("hidden");
        });
    });

    // Close modal
    closeBtn.addEventListener("click", function () {
        modal.classList.add("hidden");
    });

    // Publish alert
    sendBtn.addEventListener("click", function () {

        const message = alertMessage.value.trim();
        if (message.length === 0) {
            alert("Please enter an alert message.");
            return;
        }

        let requestBody = {
            alert_message: message,
            alert_type: selectedAlertType
        };

        if (selectedAlertType === "estimation") {
            requestBody.prediction_id = selectedPredictionId;
        } else if (selectedAlertType === "prediction") {
            requestBody.street_id = selectedStreetId;
            requestBody.water_level = parseFloat(selectedWaterLevel);
        }

        fetch("/admin/publish_alert", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const alertTypeName = selectedAlertType === "estimation" ? "Estimation" : "Prediction";
                alert(`${alertTypeName} alert published successfully!`);
                modal.classList.add("hidden");
                location.reload();
            } else {
                alert("Error: " + (data.error || "Unknown error"));
            }
        })
        .catch(err => {
            console.error(err);
            alert("Failed to publish alert.");
        });
    });

});

