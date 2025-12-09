document.getElementById("changePasswordForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const oldPass = document.getElementById("oldPassword").value;
    const newPass = document.getElementById("newPassword").value;
    const confirmPass = document.getElementById("confirmPassword").value;

    if (newPass !== confirmPass) {
        alert("Passwords do not match!");
        return;
    }

    fetch("/user-profile/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            old_password: oldPass,
            new_password: newPass
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert("Password updated!");
            window.location.href = "/user-profile/profile";
        } else {
            alert(data.error || "Error updating password.");
        }
    });
});
