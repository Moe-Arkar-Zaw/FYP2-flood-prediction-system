document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const loginBtn = document.getElementById("loginBtn");
    const loginMessage = document.getElementById("loginMessage");

    loginForm.addEventListener("submit", async function(e) {
        e.preventDefault();

        loginBtn.disabled = true;
        loginBtn.textContent = "Logging in...";
        loginMessage.textContent = "";

        const data = {
            email: document.getElementById("email").value.trim(),
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log("Login result:", result)

            if (response.ok) {
                loginMessage.style.color = "#155724";
                loginMessage.textContent = result.message;

                // Redirect immediately based on role
                if (result.role && result.role.toLowerCase() === "admin") {
                    window.location.href = "/admin/upload_video";  // Admin page
                } else {
                    window.location.href = "/user/public_dashboard";  // Public page
                }
            } else {
                loginMessage.style.color = "#721c24";
                loginMessage.textContent = result.error || "Login failed!";
            }

        } catch (err) {
            console.error(err);
            loginMessage.style.color = "#721c24";
            loginMessage.textContent = "Unexpected error occurred!";
        } finally {
            loginBtn.disabled = false;
            loginBtn.textContent = "Log In";
        }
    });
});
