document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("profileImageInput");
    const form = document.getElementById("uploadImageForm");

    fileInput.addEventListener("change", function () {

        const formData = new FormData(form);

        fetch("/user-profile/upload-profile-image", {
            method: "POST",
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert("Profile picture updated!");
                location.reload();
            } else {
                alert("Upload failed.");
            }
        });
    });

});
