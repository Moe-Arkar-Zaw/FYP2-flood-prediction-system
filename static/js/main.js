document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".nav-inner");
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.querySelectorAll(".nav-links a[data-route]");
    const profileMenu = document.querySelector(".profile-menu");
    const profileTrigger = document.querySelector(".profile-trigger");

    if (navToggle && nav) {
        navToggle.addEventListener("click", () => {
            nav.classList.toggle("open");
        });
    }

    if (navLinks.length) {
        let path = window.location.pathname;
        if (path === "/") path = "/dashboard"; // treat home as dashboard

        navLinks.forEach((link) => {
            const route = link.dataset.route;
            if (path.startsWith(route)) {
                link.classList.add("active");
            }
        });
    }

    if (profileMenu && profileTrigger) {
        profileTrigger.addEventListener("click", (e) => {
            e.stopPropagation();
            profileMenu.classList.toggle("open");
        });

        document.addEventListener("click", () => {
            profileMenu.classList.remove("open");
        });
    }

    const flashMessages = document.querySelectorAll(".flash-message");
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach((msg) => (msg.style.opacity = "0"));
        }, 3500);
    }

    window.postJSON = async function (url, data = {}) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            return await response.json();
        } catch (err) {
            console.error("POST JSON Error:", err);
            alert("Something went wrong.");
        }
    };
});
