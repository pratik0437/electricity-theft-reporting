// PowerGuard Role-Based Frontend Controller (Citizen, Vigilance Officer, Admin)

let currentUser = null;
let selectedLoginRole = "CITIZEN";
let isCitizenRegisterMode = false;
let uploadedEvidenceBase64 = null;
let uploadedEvidenceName = null;
let cachedReports = [];
let cachedOfficers = [];
let lastCreatedRefId = null;

const CATEGORY_LABELS = {
    DIRECT_HOOKING: "Direct Line Hooking (Kundi)",
    METER_TAMPERING: "Meter Tampering / Bypass",
    ILLEGAL_SUB_METERING: "Illegal Commercial Sub-Metering",
    TRANSFORMER_TAP: "Unauthorized Transformer Tap",
    SEAL_BROKEN: "Broken / Forged Meter Seal",
    UNDERGROUND_CABLE_TAP: "Underground Cable Splicing",
    OTHER: "Other Suspicious Consumption"
};

const STATUS_LABELS = {
    SUBMITTED: "Submitted (Pending Assignment)",
    UNDER_INVESTIGATION: "Assigned & Under Investigation",
    TEAM_DISPATCHED: "Field Team Dispatched",
    RESOLVED_CONFIRMED: "Resolved (Theft Confirmed)",
    DISMISSED: "Dismissed (No Violation)"
};

document.addEventListener("DOMContentLoaded", () => {
    selectLoginRole("CITIZEN");
    const saved = sessionStorage.getItem("pg_current_user");
    if (saved) {
        try {
            currentUser = JSON.parse(saved);
            enterApplicationForRole();
        } catch (_) {
            sessionStorage.removeItem("pg_current_user");
        }
    }
});

// ================= LOGIN & AUTHENTICATION =================

function selectLoginRole(role) {
    selectedLoginRole = role;
    isCitizenRegisterMode = false;
    document.getElementById("login-form").style.display = "block";
    document.getElementById("register-form").style.display = "none";

    ["CITIZEN", "OFFICER", "ADMIN"].forEach(r => {
        document.getElementById(`login-tab-${r}`).classList.toggle("active", r === role);
    });

    const regToggleBox = document.getElementById("citizen-register-toggle-box");
    regToggleBox.style.display = role === "CITIZEN" ? "block" : "none";
    document.getElementById("toggle-reg-btn").textContent = "New Citizen? Create an Account";

    const roleTitles = {
        CITIZEN: "Sign In as Citizen",
        OFFICER: "Sign In as Vigilance Officer",
        ADMIN: "Sign In as Administrator"
    };
    document.getElementById("auth-card-title").textContent = "Sign In to Portal";
    document.getElementById("auth-card-subtitle").textContent = "Select your portal role and enter your credentials";
    document.getElementById("login-submit-btn").innerHTML = `&#128274; ${roleTitles[role]}`;
}

function toggleCitizenRegisterMode() {
    isCitizenRegisterMode = !isCitizenRegisterMode;
    document.getElementById("login-form").style.display = isCitizenRegisterMode ? "none" : "block";
    document.getElementById("register-form").style.display = isCitizenRegisterMode ? "block" : "none";

    if (isCitizenRegisterMode) {
        document.getElementById("auth-card-title").textContent = "Create Citizen Account";
        document.getElementById("auth-card-subtitle").textContent = "Register to submit and track electricity theft complaints";
        document.getElementById("toggle-reg-btn").textContent = "Already have an account? Sign In";
    } else {
        document.getElementById("auth-card-title").textContent = "Sign In to Portal";
        document.getElementById("auth-card-subtitle").textContent = "Select your portal role and enter your credentials";
        document.getElementById("toggle-reg-btn").textContent = "New Citizen? Create an Account";
    }
}

async function handleLoginSubmit(event) {
    event.preventDefault();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();
    await performLogin(username, password, selectedLoginRole);
}

async function performLogin(username, password, role) {
    try {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password, role })
        });
        const json = await res.json();
        if (!res.ok || !json.success || !json.data) {
            showToast(json.message || "Invalid login credentials.");
            return;
        }

        currentUser = json.data.user;
        sessionStorage.setItem("pg_current_user", JSON.stringify(currentUser));
        showToast(json.message);
        await enterApplicationForRole();
    } catch (e) {
        showToast("Login error: " + e.message);
    }
}

async function handleRegisterSubmit(event) {
    event.preventDefault();
    const payload = {
        fullName: document.getElementById("reg-fullname").value.trim(),
        username: document.getElementById("reg-username").value.trim(),
        password: document.getElementById("reg-password").value.trim(),
        phone: document.getElementById("reg-phone").value.trim(),
        email: ""
    };

    try {
        const res = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (!res.ok || !json.success || !json.data) {
            showToast(json.message || "Registration failed.");
            return;
        }

        currentUser = json.data.user;
        sessionStorage.setItem("pg_current_user", JSON.stringify(currentUser));
        showToast(json.message);
        await enterApplicationForRole();
    } catch (e) {
        showToast("Registration error: " + e.message);
    }
}

function logoutAndShowLogin() {
    currentUser = null;
    sessionStorage.removeItem("pg_current_user");
    document.getElementById("login-form").reset();
    document.getElementById("app-shell").style.display = "none";
    document.getElementById("login-screen").style.display = "flex";
    selectLoginRole(selectedLoginRole);
}

async function enterApplicationForRole() {
    if (!currentUser) return;

    document.getElementById("login-screen").style.display = "none";
    document.getElementById("app-shell").style.display = "block";

    document.getElementById("session-user-name").textContent = currentUser.fullName;
    const roleBadge = document.getElementById("session-role-badge");
    roleBadge.className = `badge role-pill-${currentUser.role}`;
    roleBadge.textContent = currentUser.role === "CITIZEN"
        ? "Citizen"
        : currentUser.role === "OFFICER"
            ? `Vigilance Officer ${currentUser.badgeNumber ? '(' + currentUser.badgeNumber + ')' : ''}`
            : "Administrator";

    const btnReport = document.getElementById("nav-btn-report");
    const btnOfficer = document.getElementById("nav-btn-officer");
    const btnAdmin = document.getElementById("nav-btn-admin");
    const btnTrack = document.getElementById("nav-btn-track");
    const kpiBanner = document.getElementById("staff-kpi-banner");
    const subtitle = document.getElementById("header-role-subtitle");

    if (currentUser.role === "CITIZEN") {
        btnReport.style.display = "inline-flex";
        btnTrack.style.display = "inline-flex";
        btnOfficer.style.display = "none";
        btnAdmin.style.display = "none";
        kpiBanner.style.display = "none";
        subtitle.textContent = "Citizen Reporting & Status Tracking Portal";
        document.getElementById("reporterName").value = currentUser.fullName || "";
        document.getElementById("reporterPhone").value = currentUser.phone || "";
        document.getElementById("reporterEmail").value = currentUser.email || "";
    } else if (currentUser.role === "OFFICER") {
        btnReport.style.display = "none";
        btnOfficer.style.display = "inline-flex";
        btnAdmin.style.display = "none";
        btnTrack.style.display = "inline-flex";
        kpiBanner.style.display = "grid";
        subtitle.textContent = "Vigilance Officer Field Investigation Portal";
        document.getElementById("officer-desk-subtitle").textContent =
            `Assigned electricity theft reports for ${currentUser.fullName}`;
    } else if (currentUser.role === "ADMIN") {
        btnReport.style.display = "none";
        btnOfficer.style.display = "none";
        btnAdmin.style.display = "inline-flex";
        btnTrack.style.display = "inline-flex";
        kpiBanner.style.display = "grid";
        subtitle.textContent = "Administrator Portal — Officer Assignment & Case Oversight";
    }

    await refreshAllData();

    if (currentUser.role === "CITIZEN") {
        switchTab("report");
    } else if (currentUser.role === "OFFICER") {
        switchTab("officer");
    } else {
        switchTab("admin");
    }
}

// ================= DATA LOADING & SYNCHRONIZATION =================

async function refreshAllData() {
    await Promise.all([
        loadDashboardStats(),
        loadOfficers(),
        loadAllReports()
    ]);
}

function switchTab(tabName) {
    if (currentUser) {
        if (currentUser.role === "CITIZEN" && (tabName === "admin" || tabName === "officer")) {
            return;
        }
        if (currentUser.role === "OFFICER" && (tabName === "admin" || tabName === "report")) {
            tabName = "officer";
        }
        if (currentUser.role === "ADMIN" && (tabName === "officer" || tabName === "report")) {
            tabName = "admin";
        }
    }

    document.querySelectorAll(".nav-tab").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.tab === tabName);
    });
    document.querySelectorAll(".tab-section").forEach(sec => {
        sec.classList.toggle("active", sec.id === `tab-${tabName}`);
    });

    refreshAllData();
}


function detectGpsLocation() {
    const gpsInput = document.getElementById("gpsCoordinates");
    if (navigator.geolocation) {
        gpsInput.value = "Locating...";
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                gpsInput.value = `${pos.coords.latitude.toFixed(4)}, ${pos.coords.longitude.toFixed(4)}`;
                showToast("GPS coordinates captured.");
            },
            () => {
                gpsInput.value = "";
                showToast("Unable to retrieve browser GPS location. Please enter coordinates manually.");
            },
            { timeout: 4000 }
        );
    } else {
        showToast("Geolocation is not supported by this browser.");
    }
}

function handleEvidenceUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (file.size > 4 * 1024 * 1024) {
        showToast("Please choose an image smaller than 4 MB.");
        return;
    }

    uploadedEvidenceName = file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedEvidenceBase64 = e.target.result;
        const preview = document.getElementById("evidence-preview");
        preview.src = uploadedEvidenceBase64;
        preview.style.display = "inline-block";
        document.getElementById("evidence-prompt").innerHTML =
            `<strong>&#9989; Attached: ${escapeHtml(file.name)}</strong><p style="font-size:0.75rem;color:#94a3b8;">Click to replace image</p>`;
    };
    reader.readAsDataURL(file);
}

function clearEvidencePreview() {
    uploadedEvidenceBase64 = null;
    uploadedEvidenceName = null;
    const preview = document.getElementById("evidence-preview");
    preview.src = "";
    preview.style.display = "none";
    document.getElementById("evidence-prompt").innerHTML =
        `<strong>&#128247; Click to attach photo of illegal hooking, bypassed meter, or pole ID</strong>
         <p style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.25rem;">Attached evidence will be reviewed by the Administrator and assigned Vigilance Officer</p>`;
}

// CITIZEN SUBMITS REPORT
async function submitTheftReport(event) {
    event.preventDefault();
    const btn = document.getElementById("submit-report-btn");
    btn.disabled = true;
    btn.textContent = "Submitting...";

    const payload = {
        title: document.getElementById("title").value.trim(),
        category: document.getElementById("category").value,
        severity: document.getElementById("severity").value,
        address: document.getElementById("address").value.trim(),
        landmark: document.getElementById("landmark").value.trim(),
        gpsCoordinates: document.getElementById("gpsCoordinates").value.trim() || null,
        suspectConsumerNumber: document.getElementById("suspectConsumerNumber").value.trim() || null,
        description: document.getElementById("description").value.trim(),
        evidenceImageData: uploadedEvidenceBase64,
        evidenceFileName: uploadedEvidenceName,
        isAnonymous: false,
        submittedByUsername: currentUser ? currentUser.username : "citizen",
        reporterName: document.getElementById("reporterName").value.trim(),
        reporterPhone: document.getElementById("reporterPhone").value.trim(),
        reporterEmail: document.getElementById("reporterEmail").value.trim()
    };

    try {
        const res = await fetch("/api/reports", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        if (!res.ok || !result.success) {
            throw new Error(result.message || "Failed to submit report");
        }

        lastCreatedRefId = result.data.referenceId;
        document.getElementById("modal-created-ref").textContent = lastCreatedRefId;
        document.getElementById("report-form").reset();
        clearEvidencePreview();
        if (currentUser && currentUser.role === "CITIZEN") {
            document.getElementById("reporterName").value = currentUser.fullName || "";
            document.getElementById("reporterPhone").value = currentUser.phone || "";
            document.getElementById("reporterEmail").value = currentUser.email || "";
        }
        openModal("success-modal");
        await refreshAllData();
        showToast(`Complaint ${lastCreatedRefId} submitted successfully.`);
    } catch (err) {
        showToast(`Error: ${err.message}`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = "&#128680; Submit Report";
    }
}

function copyCreatedRefId() {
    if (!lastCreatedRefId) return;
    navigator.clipboard.writeText(lastCreatedRefId);
    showToast(`Copied Reference ID: ${lastCreatedRefId}`);
}

function trackCreatedReportNow() {
    closeModal("success-modal");
    switchTab("track");
    if (lastCreatedRefId) {
        document.getElementById("track-input").value = lastCreatedRefId;
        lookupReportByRefId(lastCreatedRefId);
    }
}

// DASHBOARD STATS & CHARTS
async function loadDashboardStats() {
    try {
        const res = await fetch("/api/stats");
        const json = await res.json();
        if (!json.success || !json.data) return;
        const s = json.data;

        document.getElementById("kpi-total").textContent = s.totalReports;
        document.getElementById("kpi-unassigned").textContent = s.unassignedCases ?? s.pendingCases;
        document.getElementById("admin-unassigned-pill").textContent = `${s.unassignedCases ?? s.pendingCases} Unassigned`;
        document.getElementById("kpi-active").textContent = s.activeInvestigations;
        document.getElementById("kpi-resolved").textContent = s.resolvedCases;
        document.getElementById("kpi-dismissed").textContent = s.dismissedCases;

        renderHorizontalBars("chart-categories", s.categoryBreakdown, s.totalReports);
        renderHorizontalBars("chart-statuses", s.statusBreakdown, s.totalReports);
    } catch (e) {
        console.error("Failed to load stats:", e);
    }
}

function renderHorizontalBars(containerId, mapData, total) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const entries = Object.entries(mapData || {}).filter(([_, count]) => count > 0);
    if (entries.length === 0) {
        container.innerHTML = `<p style="color:var(--text-secondary);font-size:0.88rem;padding:0.5rem 0;">No reports recorded yet.</p>`;
        return;
    }

    container.innerHTML = entries
        .sort((a, b) => b[1] - a[1])
        .map(([label, count]) => {
            const pct = total > 0 ? Math.round((count / total) * 100) : 0;
            return `
                <div class="bar-row">
                    <div class="bar-label-line">
                        <span>${escapeHtml(label)}</span>
                        <strong>${count} (${pct}%)</strong>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${Math.max(pct, 6)}%;"></div>
                    </div>
                </div>
            `;
        })
        .join("");
}

async function loadOfficers() {
    try {
        const res = await fetch("/api/officers");
        const json = await res.json();
        if (json.success && json.data) {
            cachedOfficers = json.data;
            const select = document.getElementById("admin-select-officer");
            select.innerHTML = `<option value="">-- Select Vigilance Officer --</option>` +
                cachedOfficers.map(o =>
                    `<option value="${escapeHtml(o.username)}">${escapeHtml(o.name)} — ${escapeHtml(o.designation)} (${escapeHtml(o.badgeNumber)})</option>`
                ).join("");
        }
    } catch (e) {
        console.error("Failed to load officers:", e);
    }
}

// LOAD REPORTS FOR CITIZEN, OFFICER, AND ADMIN VIEWS
async function loadAllReports() {
    const search = document.getElementById("filter-search")?.value || "";
    const status = document.getElementById("filter-status")?.value || "ALL";
    const severity = document.getElementById("filter-severity")?.value || "ALL";

    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (status !== "ALL") params.set("status", status);
    if (severity !== "ALL") params.set("severity", severity);

    try {
        const res = await fetch(`/api/reports?${params.toString()}`);
        const json = await res.json();
        if (!json.success || !json.data) return;
        cachedReports = json.data;

        renderAdminTable(cachedReports);
        renderOfficerTable();
        renderCitizenMyReports(cachedReports);
        renderQuickRefPills(cachedReports);
    } catch (e) {
        console.error("Error loading reports:", e);
    }
}

function renderCitizenMyReports(reports) {
    const container = document.getElementById("citizen-my-reports");
    if (!container) return;

    const myReports = currentUser
        ? reports.filter(r => r.submittedByUsername === currentUser.username)
        : [];

    if (myReports.length === 0) {
        container.innerHTML = `
            <div style="background: var(--bg-input); border: 1px dashed var(--border-highlight); padding: 1.5rem; border-radius: 10px; text-align: center; color: var(--text-secondary); font-size: 0.88rem;">
                You have not submitted any electricity theft reports yet. Submit a report using the form on the left.
            </div>
        `;
        return;
    }

    container.innerHTML = myReports.map(r => {
        const photoThumb = r.evidenceImageData
            ? `<img src="${r.evidenceImageData}" alt="Evidence" style="width:54px; height:54px; object-fit:cover; border-radius:8px; border:1px solid rgba(245, 158, 11, 0.4); cursor:pointer; flex-shrink:0;" onclick="jumpToTracker('${escapeHtml(r.referenceId)}')" title="Click to track report" />`
            : `<div style="width:54px; height:54px; border-radius:8px; background:rgba(255,255,255,0.04); border:1px dashed var(--border-highlight); display:flex; align-items:center; justify-content:center; color:var(--text-secondary); font-size:0.7rem; flex-shrink:0; text-align:center;">No Photo</div>`;

        return `
        <div style="background: var(--bg-input); border: 1px solid var(--border-highlight); padding: 1rem; border-radius: 10px; display:flex; gap:0.85rem; align-items:flex-start;">
            ${photoThumb}
            <div style="flex:1; min-width:0;">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                    <span class="ref-code" style="cursor:pointer;" onclick="jumpToTracker('${escapeHtml(r.referenceId)}')">${escapeHtml(r.referenceId)}</span>
                    <span class="badge badge-${r.status}" style="font-size:0.72rem;">${escapeHtml(STATUS_LABELS[r.status] || r.status)}</span>
                </div>
                <div style="font-size:0.92rem; font-weight:700; margin-top:0.35rem;">${escapeHtml(r.title)}</div>
                <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.2rem;">
                    Address: ${escapeHtml(r.address)}
                </div>
                <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.15rem;">
                    Assigned Officer: <strong style="color:#f8fafc;">${escapeHtml(r.assignedOfficer || "Pending Administrator Assignment")}</strong>
                </div>
                <div style="margin-top:0.65rem; display:flex; justify-content:flex-end;">
                    <button class="btn btn-secondary btn-sm" onclick="jumpToTracker('${escapeHtml(r.referenceId)}')">
                        &#128269; Track Progress
                    </button>
                </div>
            </div>
        </div>
        `;
    }).join("");
}

function renderOfficerTable() {
    const tbody = document.getElementById("officer-reports-tbody");
    if (!tbody) return;

    const scope = document.getElementById("officer-scope-filter")?.value || "MINE";
    let officerCases = cachedReports.filter(r => r.assignedOfficer && r.assignedOfficer.trim() !== "");

    if (currentUser && currentUser.role === "OFFICER") {
        const myAssignedCount = cachedReports.filter(r =>
            r.assignedOfficerUsername === currentUser.username ||
            r.assignedOfficer === currentUser.fullName
        ).length;
        document.getElementById("officer-assigned-pill").textContent = `${myAssignedCount} Assigned`;

        if (scope === "MINE") {
            officerCases = cachedReports.filter(r =>
                r.assignedOfficerUsername === currentUser.username ||
                r.assignedOfficer === currentUser.fullName
            );
        }
    }

    if (officerCases.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center; padding: 2.5rem; color: var(--text-secondary);">
                    No reports are currently assigned to you for investigation.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = officerCases.map(r => {
        const photoThumb = r.evidenceImageData
            ? `<img src="${r.evidenceImageData}" alt="Evidence" style="width:48px; height:48px; object-fit:cover; border-radius:6px; border:1px solid rgba(245, 158, 11, 0.4); cursor:pointer; flex-shrink:0;" onclick="openInspectModal('${escapeHtml(r.referenceId)}')" title="Click to inspect evidence" />`
            : `<div style="width:48px; height:48px; border-radius:6px; background:rgba(255,255,255,0.04); border:1px dashed var(--border-highlight); display:flex; align-items:center; justify-content:center; color:var(--text-secondary); font-size:0.7rem; flex-shrink:0; text-align:center;">No Photo</div>`;

        return `
        <tr>
            <td>
                <span class="ref-code">${escapeHtml(r.referenceId)}</span>
                <div style="font-size:0.74rem; color:var(--text-secondary); margin-top:2px;">${escapeHtml(r.createdAt)}</div>
            </td>
            <td>
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    ${photoThumb}
                    <div>
                        <div style="font-weight:700; color:var(--text-primary);">${escapeHtml(r.title)}</div>
                        <div style="font-size:0.78rem; color:var(--accent-amber);">
                            ${escapeHtml(CATEGORY_LABELS[r.category] || r.category)}
                        </div>
                    </div>
                </div>
            </td>
            <td>
                <div style="font-weight:600;">${escapeHtml(r.address)}</div>
                <div style="font-size:0.78rem; color:var(--text-secondary);">${escapeHtml(r.landmark)}</div>
            </td>
            <td><span class="badge sev-${r.severity}">${r.severity}</span></td>
            <td><span class="badge badge-${r.status}">${escapeHtml(STATUS_LABELS[r.status] || r.status)}</span></td>
            <td style="font-size:0.85rem;">
                <strong style="color:var(--accent-blue);">${escapeHtml(r.assignedOfficer || "Unassigned")}</strong>
            </td>
            <td>
                <button class="btn btn-primary btn-sm" onclick="openInspectModal('${escapeHtml(r.referenceId)}')">
                    &#128300; Investigate Case
                </button>
            </td>
        </tr>
        `;
    }).join("");
}

function renderAdminTable(reports) {
    const tbody = document.getElementById("admin-reports-tbody");
    if (!tbody) return;

    if (reports.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align:center; padding: 2.5rem; color: var(--text-secondary);">
                    No electricity theft reports have been submitted yet.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = reports.map(r => {
        const isUnassigned = !r.assignedOfficer;
        const officerBadge = isUnassigned
            ? `<span class="badge sev-CRITICAL">Unassigned — Needs Officer</span>`
            : `<strong style="color:#38bdf8;">&#128110; ${escapeHtml(r.assignedOfficer)}</strong>`;

        const btnLabel = isUnassigned ? "&#128203; Assign Officer" : "&#128260; Reassign / View";
        const btnClass = isUnassigned ? "btn btn-primary btn-sm" : "btn btn-secondary btn-sm";

        const photoThumb = r.evidenceImageData
            ? `<img src="${r.evidenceImageData}" alt="Evidence" style="width:48px; height:48px; object-fit:cover; border-radius:6px; border:1px solid rgba(245, 158, 11, 0.4); cursor:pointer; flex-shrink:0;" onclick="openInspectModal('${escapeHtml(r.referenceId)}')" title="Click to view full photo evidence" />`
            : `<div style="width:48px; height:48px; border-radius:6px; background:rgba(255,255,255,0.04); border:1px dashed var(--border-highlight); display:flex; align-items:center; justify-content:center; color:var(--text-secondary); font-size:0.7rem; flex-shrink:0; text-align:center;">No Photo</div>`;

        return `
            <tr>
                <td>
                    <span class="ref-code">${escapeHtml(r.referenceId)}</span>
                    <div style="font-size:0.74rem; color:var(--text-secondary); margin-top:2px;">${escapeHtml(r.createdAt)}</div>
                </td>
                <td>
                    <div style="display:flex; align-items:center; gap:0.75rem;">
                        ${photoThumb}
                        <div>
                            <div style="font-weight:700; color:var(--text-primary);">${escapeHtml(r.title)}</div>
                            <div style="font-size:0.78rem; color:var(--accent-amber);">
                                ${escapeHtml(CATEGORY_LABELS[r.category] || r.category)}
                            </div>
                        </div>
                    </div>
                </td>
                <td>
                    <div style="font-weight:600;">${escapeHtml(r.address)}</div>
                    <div style="font-size:0.78rem; color:var(--text-secondary);">${escapeHtml(r.landmark)}</div>
                </td>
                <td><span class="badge sev-${r.severity}">${r.severity}</span></td>
                <td><span class="badge badge-${r.status}">${escapeHtml(STATUS_LABELS[r.status] || r.status)}</span></td>
                <td style="font-size:0.85rem;">${officerBadge}</td>
                <td>
                    <button class="${btnClass}" onclick="openInspectModal('${escapeHtml(r.referenceId)}')">
                        ${btnLabel}
                    </button>
                </td>
            </tr>
        `;
    }).join("");
}

function renderQuickRefPills(reports) {
    const box = document.getElementById("quick-ref-pills");
    if (!box) return;
    if (reports.length === 0) {
        box.innerHTML = "";
        return;
    }
    box.innerHTML = reports.map(r =>
        `<button type="button" class="ref-pill" onclick="jumpToTracker('${escapeHtml(r.referenceId)}')">
            ${escapeHtml(r.referenceId)} (${escapeHtml(r.assignedOfficer ? r.assignedOfficer : "Pending Assignment")})
        </button>`
    ).join("");
}

function jumpToTracker(refId) {
    switchTab("track");
    document.getElementById("track-input").value = refId;
    lookupReportByRefId(refId);
}

function handleTrackSearch(event) {
    event.preventDefault();
    const refId = document.getElementById("track-input").value.trim();
    if (refId) {
        lookupReportByRefId(refId);
    }
}

async function lookupReportByRefId(refId) {
    const container = document.getElementById("tracking-result-container");
    container.style.display = "block";
    container.innerHTML = `<p style="text-align:center; color:var(--text-secondary);">Searching for Reference ID <strong>${escapeHtml(refId)}</strong>...</p>`;

    try {
        const res = await fetch(`/api/reports/track/${encodeURIComponent(refId)}`);
        const json = await res.json();
        if (!res.ok || !json.success || !json.data) {
            container.innerHTML = `
                <div style="text-align:center; padding: 1.5rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 10px;">
                    <h3 style="color:#f87171; margin-bottom:0.3rem;">&#9888; Reference ID Not Found</h3>
                    <p style="font-size:0.88rem; color:var(--text-secondary);">${escapeHtml(json.message || "No matching complaint found.")}</p>
                </div>
            `;
            return;
        }

        const d = json.data;
        const stageOrder = ["SUBMITTED", "UNDER_INVESTIGATION", "TEAM_DISPATCHED", "RESOLVED_CONFIRMED"];
        let activeIdx = stageOrder.indexOf(d.status);
        if (d.status === "DISMISSED") activeIdx = 3;

        const stepsHtml = [
            { label: "Citizen Reported", sub: "Step 1" },
            { label: "Assigned to Officer", sub: "Step 2" },
            { label: "Field Inspection", sub: "Step 3" },
            { label: d.status === "DISMISSED" ? "Closed (Dismissed)" : "Action Completed", sub: "Step 4" }
        ].map((st, idx) => {
            let cls = "step-item";
            if (idx < activeIdx) cls += " completed";
            else if (idx === activeIdx) cls += " current";
            return `
                <div class="${cls}">
                    <div class="step-num">${st.sub}</div>
                    <div class="step-label">${st.label}</div>
                </div>
            `;
        }).join("");

        const timelineHtml = (d.history || []).slice().reverse().map(h => `
            <div class="timeline-item">
                <div class="timeline-meta">
                    <strong>${escapeHtml(h.timestamp)}</strong>
                    <span class="badge badge-${h.status}">${escapeHtml(STATUS_LABELS[h.status] || h.status)}</span>
                    <span>by <em>${escapeHtml(h.updatedBy)}</em></span>
                </div>
                <div class="timeline-remarks">${escapeHtml(h.remarks)}</div>
            </div>
        `).join("");

        container.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:1rem;">
                <div>
                    <span class="ref-code" style="font-size:1.25rem;">${escapeHtml(d.referenceId)}</span>
                    <h3 style="font-size:1.25rem; margin-top:0.2rem;">${escapeHtml(d.title)}</h3>
                </div>
                <div style="display:flex; gap:0.5rem; align-items:center;">
                    <span class="badge sev-${d.severity}">Severity: ${d.severity}</span>
                    <span class="badge badge-${d.status}">${escapeHtml(d.statusDisplay)}</span>
                </div>
            </div>

            <div class="progress-stepper">${stepsHtml}</div>

            <div class="info-kv-grid">
                <div class="info-kv"><span>Theft Category</span><strong>${escapeHtml(d.categoryDisplay)}</strong></div>
                <div class="info-kv"><span>Premises Address</span><strong>${escapeHtml(d.address)}</strong></div>
                <div class="info-kv"><span>Landmark / Pole</span><strong>${escapeHtml(d.landmark)}</strong></div>
                <div class="info-kv"><span>Assigned Vigilance Officer</span><strong style="color:var(--accent-blue);">${escapeHtml(d.assignedOfficer)}</strong></div>
                <div class="info-kv"><span>Last Updated</span><strong>${escapeHtml(d.updatedAt)}</strong></div>
            </div>

            <div style="margin-bottom:1.25rem;">
                <label>Latest Official Remarks</label>
                <div style="background:var(--bg-input); padding:0.9rem; border-radius:8px; border-left:4px solid var(--accent-amber); font-size:0.9rem;">
                    ${escapeHtml(d.inspectionNotes)}
                </div>
            </div>

            <div>
                <label style="margin-bottom:0.75rem;">Chronological Assignment &amp; Investigation History</label>
                <div class="timeline">${timelineHtml}</div>
            </div>
        `;
    } catch (e) {
        container.innerHTML = `<p style="color:#f87171;">Error fetching tracking details: ${escapeHtml(e.message)}</p>`;
    }
}

// MODAL: OPEN FOR ADMIN ASSIGNMENT OR OFFICER INVESTIGATION
async function openInspectModal(refId) {
    try {
        const res = await fetch(`/api/reports/${encodeURIComponent(refId)}`);
        const json = await res.json();
        if (!json.success || !json.data) {
            showToast("Could not load report details.");
            return;
        }
        const r = json.data;

        document.getElementById("ins-ref-id").textContent = r.referenceId;
        document.getElementById("ins-title").textContent = r.title;

        const adminForm = document.getElementById("admin-assign-form");
        const officerForm = document.getElementById("officer-investigate-form");

        if (currentUser && currentUser.role === "ADMIN") {
            adminForm.style.display = "block";
            officerForm.style.display = "none";
            document.getElementById("admin-assign-ref-id").value = r.referenceId;
            document.getElementById("admin-select-severity").value = r.severity;
            const matchedOff = cachedOfficers.find(o => o.username === r.assignedOfficerUsername || o.name === r.assignedOfficer);
            document.getElementById("admin-select-officer").value = matchedOff ? matchedOff.username : "";
            document.getElementById("admin-assign-remarks").value = r.inspectionNotes && r.assignedOfficer ? r.inspectionNotes : "";
        } else if (currentUser && currentUser.role === "OFFICER") {
            adminForm.style.display = "none";
            officerForm.style.display = "block";
            document.getElementById("officer-inv-ref-id").value = r.referenceId;
            document.getElementById("officer-inv-status").value =
                r.status === "SUBMITTED" ? "UNDER_INVESTIGATION" : r.status;
            document.getElementById("officer-inv-notes").value = r.inspectionNotes || "";
        } else {
            adminForm.style.display = "none";
            officerForm.style.display = "none";
        }

        const reporterInfo = `${escapeHtml(r.reporterName || r.submittedByUsername || "Citizen")}${r.reporterPhone ? ' &bull; ' + escapeHtml(r.reporterPhone) : ''}${r.reporterEmail ? ' &bull; ' + escapeHtml(r.reporterEmail) : ''}`;

        document.getElementById("ins-kv-grid").innerHTML = `
            <div class="info-kv"><span>Category</span><strong>${escapeHtml(CATEGORY_LABELS[r.category] || r.category)}</strong></div>
            <div class="info-kv"><span>Severity</span><strong><span class="badge sev-${r.severity}">${r.severity}</span></strong></div>
            <div class="info-kv"><span>Premises Address</span><strong>${escapeHtml(r.address)}</strong></div>
            <div class="info-kv"><span>Nearest Pole / Landmark</span><strong>${escapeHtml(r.landmark || "N/A")}</strong></div>
            <div class="info-kv"><span>Suspect Consumer / Pole #</span><strong>${escapeHtml(r.suspectConsumerNumber || "Not Provided")}</strong></div>
            <div class="info-kv"><span>GPS Coordinates</span><strong>${escapeHtml(r.gpsCoordinates || "Not Provided")}</strong></div>
            <div class="info-kv"><span>Assigned Officer</span><strong style="color:var(--accent-blue);">${escapeHtml(r.assignedOfficer || "Unassigned")}</strong></div>
            <div class="info-kv"><span>Reporter Identity</span><strong>${reporterInfo}</strong></div>
        `;

        document.getElementById("ins-description").textContent = r.description;

        const evBox = document.getElementById("ins-evidence-box");
        const evImg = document.getElementById("ins-evidence-img");
        if (r.evidenceImageData) {
            evImg.src = r.evidenceImageData;
            evBox.style.display = "block";
        } else {
            evBox.style.display = "none";
        }

        const timelineHtml = (r.history || []).slice().reverse().map(h => `
            <div class="timeline-item">
                <div class="timeline-meta">
                    <strong>${escapeHtml(h.timestamp)}</strong>
                    <span class="badge badge-${h.status}">${escapeHtml(STATUS_LABELS[h.status] || h.status)}</span>
                    <span>by <em>${escapeHtml(h.updatedBy)}</em></span>
                </div>
                <div class="timeline-remarks">${escapeHtml(h.remarks)}</div>
            </div>
        `).join("");
        document.getElementById("ins-timeline").innerHTML = timelineHtml;

        openModal("inspect-modal");
    } catch (e) {
        showToast("Error loading case details: " + e.message);
    }
}

// ADMIN SUBMITS OFFICER ASSIGNMENT
async function submitAdminAssignOfficer(event) {
    event.preventDefault();
    const refId = document.getElementById("admin-assign-ref-id").value;
    const officerUsername = document.getElementById("admin-select-officer").value;
    const officerObj = cachedOfficers.find(o => o.username === officerUsername);

    const payload = {
        assignedOfficer: officerObj ? officerObj.name : officerUsername,
        assignedOfficerUsername: officerUsername,
        severity: document.getElementById("admin-select-severity").value,
        adminRemarks: document.getElementById("admin-assign-remarks").value.trim(),
        updatedBy: currentUser ? currentUser.fullName : "Administrator"
    };

    try {
        const res = await fetch(`/api/reports/${encodeURIComponent(refId)}/assign`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (!res.ok || !json.success) {
            throw new Error(json.message || "Officer assignment failed");
        }
        closeModal("inspect-modal");
        await refreshAllData();
        showToast(json.message);
    } catch (e) {
        showToast("Error: " + e.message);
    }
}

// OFFICER SUBMITS FIELD INVESTIGATION UPDATE
async function submitOfficerInvestigation(event) {
    event.preventDefault();
    const refId = document.getElementById("officer-inv-ref-id").value;
    const payload = {
        status: document.getElementById("officer-inv-status").value,
        inspectionNotes: document.getElementById("officer-inv-notes").value.trim(),
        updatedBy: currentUser ? currentUser.fullName : "Vigilance Officer"
    };

    try {
        const res = await fetch(`/api/reports/${encodeURIComponent(refId)}/investigate`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (!res.ok || !json.success) {
            throw new Error(json.message || "Investigation update failed");
        }
        closeModal("inspect-modal");
        await refreshAllData();
        showToast(json.message);
    } catch (e) {
        showToast("Error: " + e.message);
    }
}

async function deleteCurrentReport() {
    const refId = document.getElementById("admin-assign-ref-id").value;
    if (!refId) return;

    try {
        const res = await fetch(`/api/reports/${encodeURIComponent(refId)}`, {
            method: "DELETE"
        });
        const json = await res.json();
        if (json.success) {
            closeModal("inspect-modal");
            await refreshAllData();
            showToast(`Deleted report ${refId}`);
        } else {
            showToast(json.message || "Could not delete report");
        }
    } catch (e) {
        showToast("Error deleting report: " + e.message);
    }
}

function resetFilters() {
    document.getElementById("filter-search").value = "";
    document.getElementById("filter-status").value = "ALL";
    document.getElementById("filter-severity").value = "ALL";
    loadAllReports();
}

function exportReportsCsv() {
    if (!cachedReports || cachedReports.length === 0) {
        showToast("No reports to export.");
        return;
    }
    const headers = ["ReferenceID", "Title", "Category", "Severity", "Status", "Address", "Landmark", "AssignedOfficer", "CreatedAt"];
    const rows = cachedReports.map(r => [
        r.referenceId,
        `"${(r.title || "").replace(/"/g, '""')}"`,
        r.category,
        r.severity,
        r.status,
        `"${(r.address || "").replace(/"/g, '""')}"`,
        `"${(r.landmark || "").replace(/"/g, '""')}"`,
        `"${(r.assignedOfficer || "Unassigned").replace(/"/g, '""')}"`,
        r.createdAt
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const link = document.createElement("a");
    link.setAttribute("href", encodeURI(csvContent));
    link.setAttribute("download", "powerguard_vigilance_reports.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("Exported vigilance reports to CSV.");
}

function openModal(id) {
    document.getElementById(id).classList.add("open");
}

function closeModal(id) {
    document.getElementById(id).classList.remove("open");
}

function showToast(message) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3800);
}

function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
