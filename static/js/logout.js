document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault();

            fetch("/auth/logout", {       
                method: "POST"
            })
            .then(r => {
                if (r.ok) {
                    return r.json();
                }
                throw new Error("Logout failed");
            })
            .then(data => {
                // Redirect to homepage after successful logout
                window.location.href = "/public_dashboard";
            })
            .catch(() => {
                // Even if there's an error, redirect to homepage
                window.location.href = "/public_dashboard";
            });
        });
    }
});
