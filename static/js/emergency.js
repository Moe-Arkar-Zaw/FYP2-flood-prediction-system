document.addEventListener("DOMContentLoaded", function () {

    // Load Emergency Contacts

    fetch("/api/emergency/contacts")
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById("contactList");
            container.innerHTML = "";

            data.contacts.forEach(c => {
                container.innerHTML += `
                    <div class="contact-card fade-in">
                        <div class="icon">📞</div>
                        <div>
                            <strong>${c.type}</strong><br>
                            <a href="tel:${c.number}" class="call-link">${c.number}</a>
                        </div>
                    </div>
                `;
            });
        });


    //Load Nearby Shelters
    fetch("/api/emergency/shelters")
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById("shelterList");
            list.innerHTML = "";

            data.shelters.forEach(s => {
                const cap = parseInt(s.capacity);
                const barWidth = Math.min(cap / 2, 100);

                list.innerHTML += `
                    <div class="shelter-card fade-in">
                        <strong>${s.name}</strong><br>
                        <span>📍 ${s.address}</span><br>
                        <div class="capacity-bar">
                            <div class="capacity-fill" style="width:${barWidth}%"></div>
                        </div>
                        <small>Capacity: ${s.capacity}</small>
                    </div>
                `;
            });
        });


    // Load Flood Tips
    fetch("/api/emergency/safety-info")
        .then(r => r.json())
        .then(data => {
            const { before_flood, during_flood, after_flood } = data.tips;

            fillList("beforeList", before_flood);
            fillList("duringList", during_flood);
            fillList("afterList", after_flood);
        });

    function fillList(id, items) {
        const ul = document.getElementById(id);
        items.forEach(t => {
            ul.innerHTML += `<li class="fade-in">${t}</li>`;
        });
    }

    // Collapsible Animations
    document.querySelectorAll(".tip-group").forEach(group => {
        group.addEventListener("click", () => {
            group.classList.toggle("expanded");
        });
    });

});
