document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault();

            fetch("/auth/logout", {       
                method: "POST"
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/auth/login-page"; // Redirect to login page
                } else {
                    alert("Logout failed.");
                }
            })
            .catch(() => alert("Logout error"));
        });
    }
});
