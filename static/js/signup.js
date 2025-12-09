document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById("signupForm");
    const signupBtn = document.getElementById("signupBtn");
    const signupMessage = document.getElementById("signupMessage");

    signupForm.addEventListener("submit", async function(e) {
        e.preventDefault();

        signupBtn.disabled = true;
        signupBtn.textContent = "Signing up... ";
        signupMessage.textContent = "";

        const data = {
            username: document.getElementById("username").value.trim(),
            email: document.getElementById("email").value.trim(),
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                signupMessage.style.color = "#155724";
                signupMessage.textContent = result.message;
                signupForm.reset();
                signupBtn.textContent = "Sign Up ";
            } else {
                signupMessage.style.color = "#721c24";
                signupMessage.textContent = result.error || "Signup failed!";
                signupBtn.textContent = "Sign Up ";
            }

        } catch (err) {
            console.error(err);
            signupMessage.style.color = "#721c24";
            signupMessage.textContent = "Unexpected error occurred!";
            signupBtn.textContent = "Sign Up ";
        } finally {
            signupBtn.disabled = false;
        }
    });
});
