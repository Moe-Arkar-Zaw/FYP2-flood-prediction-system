document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("alertModal");
    const alertMessage = document.getElementById("alertMessage");

    const sendBtn = document.getElementById("sendAlertBtn");
    const closeBtn = document.getElementById("closeModalBtn");

    let selectedPredictionId = null;

    // Open modal
    document.querySelectorAll(".publish-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            selectedPredictionId = this.dataset.predictionId;
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

        fetch("/admin/publish_alert", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prediction_id: selectedPredictionId,
                alert_message: message
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert("Alert published successfully!");
                modal.classList.add("hidden");
                location.reload(); // optional but useful
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

