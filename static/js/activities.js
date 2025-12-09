// static/js/activities.js

document.addEventListener("DOMContentLoaded", () => {
    const artistId = document.getElementById("artist-id").value;
    loadArtistSidebar(artistId);
    loadActivitiesTimeline(artistId);
});

// Reuse same sidebar loader as dashboard
function loadArtistSidebar(artistId) {
    fetch(`/api/artists/${artistId}`)
        .then(r => r.json())
        .then(artist => {
            document.getElementById("sidebar-artist-name").textContent = artist.stageName;
            if (artist.profileImageUrl) {
                document.getElementById("sidebar-artist-image").src = artist.profileImageUrl;
            } else {
                document.getElementById("sidebar-artist-image").src =
                    "https://via.placeholder.com/80x80?text=Artist";
            }
        })
        .catch(err => console.error("Error loading artist:", err));
}

function loadActivitiesTimeline(artistId) {
    fetch(`/api/activities/artist/${artistId}`)
        .then(r => r.json())
        .then(items => {
            const container = document.getElementById("activities-timeline");
            container.innerHTML = "";

            // group by date label
            items.sort((a, b) => new Date(a.date) - new Date(b.date));

            items.forEach(act => {
                const item = document.createElement("div");
                item.className = "timeline-item";

                const dot = document.createElement("div");
                dot.className = "timeline-dot";

                const dateEl = document.createElement("div");
                dateEl.className = "timeline-date";
                dateEl.textContent = formatPrettyDate(act.date);

                const titleEl = document.createElement("div");
                titleEl.className = "timeline-title";
                titleEl.textContent = act.title;

                const metaEl = document.createElement("div");
                metaEl.className = "timeline-meta";
                let meta = "";
                if (act.type) meta += act.type;
                if (act.location) meta += meta ? " · " + act.location : act.location;
                metaEl.textContent = meta;

                item.appendChild(dot);
                item.appendChild(dateEl);
                item.appendChild(titleEl);
                item.appendChild(metaEl);

                container.appendChild(item);
            });
        })
        .catch(err => console.error("Error loading activities:", err));
}

function formatPrettyDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}
