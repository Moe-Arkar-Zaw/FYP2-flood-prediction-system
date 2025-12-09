document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadVideoForm");
    const timestampInput = document.getElementById("timestamp");
    const cancelBtn = document.getElementById("cancelUploadBtn");


    // Auto-fill timestamp
    function setLocalTimestamp() {
        const now = new Date();
        const tzOffset = now.getTimezoneOffset() * 60000;
        timestampInput.value = new Date(now - tzOffset).toISOString().slice(0, 16);
    }

    if (timestampInput) setLocalTimestamp();

    // Cancel button
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = "/admin/upload_video";
        });
    }

    // Success/Error message container
    const messageContainer = document.createElement("div");
    messageContainer.id = "uploadMessage";
    messageContainer.style.display = "none";
    messageContainer.style.marginTop = "10px";
    messageContainer.style.padding = "10px";
    messageContainer.style.borderRadius = "5px";
    messageContainer.style.fontWeight = "bold";
    messageContainer.style.transition = "0.3s ease-in-out";
    form.prepend(messageContainer);

    // AJAX form submit (NO RELOAD)
    form.addEventListener("submit", async function (e) {
        e.preventDefault(); // Prevent full page reload

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                console.log("Latest video ID:", result.video_id);

                // Styled success message
                messageContainer.style.display = "block";
                messageContainer.style.backgroundColor = "#d4edda";
                messageContainer.style.color = "#155724";
                messageContainer.textContent = " Video uploaded successfully!";

                // Reset form EXCEPT timestamp
                const oldTimestamp = timestampInput.value;
                form.reset();
                timestampInput.value = oldTimestamp;

                // Highlight for clarity
                messageContainer.style.opacity = "1";
                setTimeout(() => { messageContainer.style.opacity = "0.8"; }, 1000);

            } else {
                // Styled error message
                messageContainer.style.display = "block";
                messageContainer.style.backgroundColor = "#f8d7da";
                messageContainer.style.color = "#721c24";
                messageContainer.textContent = result.error;
            }

        } catch (err) {
            messageContainer.style.display = "block";
            messageContainer.style.backgroundColor = "#f8d7da";
            messageContainer.style.color = "#721c24";
            messageContainer.textContent = " Unexpected error occurred!";
            console.error(err);
        }
    });
});
