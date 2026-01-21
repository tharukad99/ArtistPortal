document.addEventListener("DOMContentLoaded", () => {
  // ====== GET ELEMENTS ======
  const tbody = document.getElementById("artistsTbody");
  const statusEl = document.getElementById("status");
  const searchBox = document.getElementById("searchBox");
  const btnAdd = document.getElementById("btnAdd");

  const modal = document.getElementById("artistModal");
  const backdrop = document.getElementById("modalBackdrop");
  const modalTitle = document.getElementById("modalTitle");

  const btnClose = document.getElementById("btnCloseModal");
  const btnCancel = document.getElementById("btnCancel");
  const btnSave = document.getElementById("btnSave");

  const artistId = document.getElementById("artistId");
  const stageName = document.getElementById("stageName");
  const fullName = document.getElementById("fullName");
  const country = document.getElementById("country");
  const primaryGenre = document.getElementById("primaryGenre");
  const websiteUrl = document.getElementById("websiteUrl");
  const profileImageUrl = document.getElementById("profileImageUrl");
  const bio = document.getElementById("bio");
  const isActive = document.getElementById("isActive");

  const formError = document.getElementById("formError");
  const artistsTable = document.getElementById("artistsTable");

  // ====== STATE ======
  let allArtists = [];

  // ====== UTILS ======
  function setStatus(msg) { statusEl.textContent = msg || ""; }

  function escapeHtml(str) {
    return String(str ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // ====== MODAL CONTROL ======
  function openModal(mode, artist = null) {
    console.log( "dd",artist);
    formError.textContent = "";

    if (mode === "add") {
      modalTitle.textContent = "Add Artist";
      artistId.value = "0";
      stageName.value = "";
      fullName.value = "";
      country.value = "";
      primaryGenre.value = "";
      websiteUrl.value = "";
      profileImageUrl.value = "";
      bio.value = "";
      isActive.checked = true;
    } else {
      modalTitle.textContent = "Edit Artist";
      // id.value = String(artist.id);
      artistId.value = String(artist.id);

      // These keys MUST match your API response
      stageName.value = artist.stageName || "";
      fullName.value = artist.fullName || "";
      country.value = artist.country || "";
      primaryGenre.value = artist.primaryGenre || "";
      websiteUrl.value = artist.websiteUrl || "";
      profileImageUrl.value = artist.profileImageUrl || "";
      bio.value = artist.bio || "";
      isActive.checked = !!artist.IsActive;
    }

    backdrop.hidden = false;
    modal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    backdrop.hidden = true;
    modal.hidden = true;
    document.body.style.overflow = "";
  }

  // Force hidden on load (safety)
  modal.hidden = true;
  backdrop.hidden = true;

  // ====== TABLE ======
  function renderTable(items) {
    tbody.innerHTML = "";

    if (!items.length) {
      tbody.innerHTML = `<tr><td colspan="7" class="empty">No artists found.</td></tr>`;
      return;
    }

    for (const a of items) {
      const created = a.dateCreated ? String(a.dateCreated).replace("T", " ").slice(0, 19) : "-";

      // console.log(a);
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.id}</td>
        <td>
          <div class="name-cell">
            <div class="name">${escapeHtml(a.stageName || "")}</div>
            <div class="muted">${escapeHtml(a.fullName || "")}</div>
          </div>
        </td>
        <td>${escapeHtml(a.country || "-")}</td>
        <td>${escapeHtml(a.primaryGenre || "-")}</td>
        <td>
          <span class="pill ${a.isActive ? "pill-green" : "pill-gray"}">
            ${a.isActive ? "Active" : "Inactive"}
          </span>
        </td>
        <td>${escapeHtml(created)}</td>
        <td>
          <button type="button" class="btn-small" data-action="edit" data-id="${a.id}">Edit</button>
        </td>
      `;
      tbody.appendChild(tr);
    }
  }

  function filterAndRender() {
    const q = (searchBox.value || "").trim().toLowerCase();
    const filtered = !q ? allArtists : allArtists.filter(a => (a.stageName || "").toLowerCase().includes(q));
    renderTable(filtered);
  }

  // ======Get all artists data API ======
  async function loadArtists() {
    setStatus("Loading...");
    const res = await fetch("/api/artists/AllArtistsList?only_active=0");

    if (!res.ok) {
      setStatus("Failed to load artists");
      return;
    }
    

    allArtists = await res.json();

    setStatus("");
    filterAndRender();
  }


  //save artist
  async function saveArtist() {
    formError.textContent = "";

    const payload = {
      stageName: (stageName.value || "").trim(),
      fullName: (fullName.value || "").trim(),
      country: (country.value || "").trim(),
      primaryGenre: (primaryGenre.value || "").trim(),
      websiteUrl: (websiteUrl.value || "").trim(),
      profileImageUrl: (profileImageUrl.value || "").trim(),
      bio: (bio.value || "").trim(),
      isActive: isActive.checked
    };

    if (!payload.stageName) {
      formError.textContent = "Stage Name is required.";
      return;
    }

    const id = parseInt(artistId.value || "0", 10);
    const url = id > 0 ? `/api/artists/${id}` : "/api/artists";
    const method = id > 0 ? "PUT" : "POST";

    btnSave.disabled = true;
    const oldText = btnSave.textContent;
    btnSave.textContent = "Saving...";

    try {
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        credentials: "include"
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        formError.textContent = data.message || "Save failed.";
        return;
      }

      closeModal();
      await loadArtists();
    } finally {
      btnSave.disabled = false;
      btnSave.textContent = oldText;
    }
  }

  // ====== EVENTS ======
  btnAdd.addEventListener("click", () => openModal("add"));

  btnClose.addEventListener("click", (e) => {
    e.preventDefault();
    closeModal();
  });

  btnCancel.addEventListener("click", (e) => {
    e.preventDefault();
    closeModal();
  });

  backdrop.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.hidden) closeModal();
  });

  searchBox.addEventListener("input", filterAndRender);

  artistsTable.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;

    const id = parseInt(btn.dataset.id, 10);
    // const artist = allArtists.find(a => a.ArtistId === id);
    const artist = allArtists.find(a => a.id === id);
    if (artist) openModal("edit", artist);
  });

  btnSave.addEventListener("click", saveArtist);

  // ====== START ======
  loadArtists();
});
