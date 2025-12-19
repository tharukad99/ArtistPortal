document.addEventListener("DOMContentLoaded", () => {
    const artistId = document.getElementById("artist-id")?.value;
    if (!artistId) return;

    loadArtistSidebar(artistId);
    loadArtistBio(artistId);

    loadLatestAlbumFromActivities(artistId);
    loadRecentActivities(artistId);

    loadPhotoGallery(artistId);
});

/* ---------------- Sidebar + Bio ---------------- */
function loadArtistSidebar(artistId) {
    fetch(`/api/artists/${artistId}`)
        .then(r => r.json())
        .then(artist => {
            document.getElementById("sidebar-artist-name").textContent = artist.stageName || "Artist";
            document.getElementById("sidebar-artist-image").src =
                artist.profileImageUrl || "https://via.placeholder.com/80x80?text=Artist";
        })
        .catch(err => console.error("Sidebar artist load error:", err));
}

/* ---------------- Artist Bio ---------------- */
function loadArtistBio(artistId) {
    fetch(`/api/artists/${artistId}`)
        .then(r => r.json())
        .then(artist => {
            document.getElementById("bio-stage-name").textContent = artist.stageName || "Artist";
            document.getElementById("bio-full-name").textContent = artist.fullName || "";

            const bioText = document.getElementById("bio-text");
            bioText.textContent = artist.bio && artist.bio.trim()
                ? artist.bio
                : "No biography available yet.";

            const websiteLink = document.getElementById("bio-website");
            if (artist.websiteUrl) {
                websiteLink.href = artist.websiteUrl;
                websiteLink.style.display = "inline-flex";
            } else {
                websiteLink.style.display = "none";
            }

            console.log("aa" , artist.sourcesCount);
            const sourcesCount = document.getElementById("bio-sources-count");
            if (sourcesCount) {
                sourcesCount.textContent = `Connected platforms: ${artist.sourcesCount || 0}`;
            }
        })
        .catch(err => console.error("Bio load error:", err));
}

/* ---------------- Latest Album ---------------- */
function loadLatestAlbumFromActivities(artistId) {
    fetch(`/api/activities/artist/${artistId}`)
        .then(r => r.json())
        .then(items => {
            const box = document.getElementById("latest-album");
            if (!box) return;

            if (!items || items.length === 0) {
                box.textContent = "No album data found.";
                return;
            }

            // Sort newest first
            items.sort((a, b) => new Date(b.date) - new Date(a.date));

            // Find album-like activity
            const album = items.find(a =>
                (a.type && a.type.toLowerCase().includes("album")) ||
                (a.title && a.title.toLowerCase().includes("album"))
            );

            if (!album) {
                box.textContent = "No album activity found yet.";
                return;
            }

            box.innerHTML = `
                <div style="font-weight:700; font-size:15px;">${escapeHtml(album.title)}</div>
                <div style="color:#6b7280; font-size:13px; margin-top:4px;">
                    Release Date: ${formatPrettyDate(album.date)}
                </div>
            `;
        })
        .catch(err => console.error("Latest album load error:", err));
}

/* ---------------- Recent Activities ---------------- */
function loadRecentActivities(artistId) {
    fetch(`/api/activities/artist/${artistId}`)
        .then(r => r.json())
        .then(items => {
            const container = document.getElementById("recent-activities");
            container.innerHTML = "";

            if (!items || items.length === 0) {
                container.innerHTML = "<div class='empty'>No activities found.</div>";
                return;
            }

            // Newest first
            items.sort((a, b) => new Date(b.date) - new Date(a.date));

            items.slice(0, 8).forEach(act => {
                const row = document.createElement("div");
                row.className = "activity-item";

                const left = document.createElement("div");
                left.textContent = act.title;

                const right = document.createElement("div");
                right.textContent = formatPrettyDate(act.date);

                row.appendChild(left);
                row.appendChild(right);
                container.appendChild(row);
            });
        })
        .catch(err => console.error("Activities load error:", err));
}

/* ---------------- Photo Gallery ---------------- */
function loadPhotoGallery(artistId) {
    const container = document.getElementById("photo-gallery");
    if (!container) return;

    fetch(`/api/artists/${artistId}/photos`)
        .then(r => r.json())
        .then(images => {
            container.innerHTML = "";

            if (!images || images.length === 0) {
                container.innerHTML = "<div class='empty'>No photos available.</div>";
                return;
            }

            images.slice(0, 6).forEach(img => {
                const a = document.createElement("a");
                a.href = img.url;
                a.target = "_blank";
                a.rel = "noopener noreferrer";
                a.className = "gallery-item";

                const image = document.createElement("img");
                image.src = img.url;
                image.alt = img.caption || "Artist photo";
                image.loading = "lazy";

                a.appendChild(image);
                container.appendChild(a);
            });
        })
        .catch(err => {
            // If API not ready, show message instead of breaking
            console.error("Gallery load error:", err);
            container.innerHTML = "<div class='empty'>Gallery endpoint not available yet.</div>";
        });
}

/* ---------------- Helpers ---------------- */
function formatPrettyDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}

function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/[&<>"']/g, m => ({
        "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[m]));
}
