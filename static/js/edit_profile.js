document.getElementById("editProfileForm").addEventListener("submit", function (e) {
    e.preventDefault();

    fetch("/user-profile/update-profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            full_name: document.getElementById("fullName").value,
            email: document.getElementById("email").value
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert("Profile updated!");
            window.location.href = "/user-profile/profile";
        } else {
            alert("Update failed: " + data.error);
        }
    });
});
