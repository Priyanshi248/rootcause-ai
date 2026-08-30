// Replace this with your Render backend URL before deploying the frontend.
const API_BASE = "https://rootcause-ai-backend.onrender.com";

let currentIncidentId = null;
let incidentPage = 1;
const incidentLimit = 10;
let cachedIncidents = [];

function getToken() {
  return localStorage.getItem("access_token");
}

function authHeaders(extra = {}) {
  const token = getToken();
  if (!token) throw new Error("Please login first.");
  return { ...extra, Authorization: `Bearer ${token}` };
}

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: authHeaders(headers)
  });
  const text = await response.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!response.ok) {
    const detail = data?.detail || data?.message || text || `Request failed (${response.status})`;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return data;
}

function showAuth(mode) {
  document.getElementById("login-form").classList.toggle("hidden", mode !== "login");
  document.getElementById("register-form").classList.toggle("hidden", mode !== "register");
  document.getElementById("login-tab").classList.toggle("active", mode === "login");
  document.getElementById("register-tab").classList.toggle("active", mode === "register");
}

async function login() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;
  if (!email || !password) return setMessage("login-message", "Enter email and password.", true);

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({email, password})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Login failed.");
    localStorage.setItem("access_token", data.access_token);
    await startApp();
  } catch (e) {
    setMessage("login-message", e.message, true);
  }
}

async function registerUser() {
  const full_name = document.getElementById("register-name").value.trim();
  const email = document.getElementById("register-email").value.trim();
  const password = document.getElementById("register-password").value;
  if (!full_name || !email || !password) return setMessage("register-message", "Fill in all fields.", true);

  try {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({full_name, email, password})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Registration failed.");
    setMessage("register-message", "Account created. You can now log in.", false);
    showAuth("login");
    document.getElementById("login-email").value = email;
  } catch (e) {
    setMessage("register-message", e.message, true);
  }
}

function logout() {
  localStorage.removeItem("access_token");
  currentIncidentId = null;
  document.getElementById("app-section").classList.add("hidden");
  document.getElementById("auth-section").classList.remove("hidden");
}

async function startApp() {
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("app-section").classList.remove("hidden");
  try {
    const user = await api("/auth/me");
    document.getElementById("current-user").textContent = user.full_name || user.email;
  } catch {
    logout();
    return;
  }
  showPage("dashboard");
  await loadDashboard();
  await loadIncidents();
}

function showPage(page) {
  document.querySelectorAll(".page").forEach(el => el.classList.add("hidden"));
  const target = document.getElementById(`page-${page}`);
  if (target) target.classList.remove("hidden");

  document.querySelectorAll(".nav-button").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.page === page);
  });

  if (page === "dashboard") loadDashboard();
  if (page === "incidents") loadIncidents();
  if (page === "timeline") populateIncidentSelectors().then(loadTimeline);
  if (page === "audit") populateIncidentSelectors().then(loadAudit);
}

function openCreateIncident() {
  showPage("create");
}

async function createIncident() {
  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();
  const service_name = document.getElementById("service").value.trim();
  const environment = document.getElementById("environment").value;
  const severity = document.getElementById("severity").value;

  if (!title || !description || !service_name) {
    return setMessage("incident-message", "Title, description and service are required.", true);
  }

  try {
    const incident = await api("/incidents/incidents", {
      method: "POST",
      body: JSON.stringify({title, description, service_name, environment, severity})
    });
    currentIncidentId = incident.id;
    toast("Incident created.");
    await loadDashboard();
    await loadIncidents();
    await loadIncidentDetail(incident.id);
  } catch (e) {
    setMessage("incident-message", e.message, true);
  }
}

async function loadDashboard() {
  try {
    const d = await api("/dashboard/dashboard");
    const metrics = [
      ["Total", d.total_incidents],
      ["Open", d.open_incidents],
      ["Resolved", d.resolved_incidents],
      ["Critical", d.critical_incidents],
      ["High", d.high_incidents],
      ["Medium", d.medium_incidents],
      ["Low", d.low_incidents]
    ];
    document.getElementById("dashboard-metrics").innerHTML = metrics.map(([label, value]) =>
      `<div class="metric-card"><span>${escapeHtml(label)}</span><strong>${value ?? 0}</strong></div>`
    ).join("");

    document.getElementById("severity-breakdown").innerHTML = [
      ["Critical", d.critical_incidents], ["High", d.high_incidents],
      ["Medium", d.medium_incidents], ["Low", d.low_incidents]
    ].map(([label, value]) => breakdownRow(label, value)).join("");

    document.getElementById("environment-breakdown").innerHTML = [
      ["Production", d.production_incidents], ["Staging", d.staging_incidents],
      ["Development", d.development_incidents]
    ].map(([label, value]) => breakdownRow(label, value)).join("");

    document.getElementById("recent-incidents").innerHTML = (d.recent_incidents || []).map(renderIncidentRow).join("") ||
      `<div class="empty">No incidents yet.</div>`;
  } catch (e) {
    toast(e.message, true);
  }
}

function breakdownRow(label, value) {
  return `<div class="breakdown-row"><span>${escapeHtml(label)}</span><strong>${value ?? 0}</strong></div>`;
}

async function loadIncidents() {
  try {
    const params = new URLSearchParams({
      page: incidentPage,
      limit: incidentLimit
    });
    const search = document.getElementById("incident-search")?.value.trim();
    const status = document.getElementById("filter-status")?.value;
    const severity = document.getElementById("filter-severity")?.value;
    const environment = document.getElementById("filter-environment")?.value;
    if (search) params.set("search", search);
    if (status) params.set("status", status);
    if (severity) params.set("severity", severity);
    if (environment) params.set("environment", environment);

    const data = await api(`/incidents/incidents?${params.toString()}`);
    const incidents = Array.isArray(data) ? data : (data?.items || data?.incidents || []);
    cachedIncidents = incidents;
    document.getElementById("incident-list").innerHTML =
      incidents.map(renderIncidentRow).join("") || `<div class="empty">No incidents found.</div>`;
    document.getElementById("incident-page").textContent = `Page ${incidentPage}`;
    await populateIncidentSelectors();
  } catch (e) {
    toast(e.message, true);
  }
}

function changeIncidentPage(delta) {
  incidentPage = Math.max(1, incidentPage + delta);
  loadIncidents();
}

function renderIncidentRow(i) {
  return `
    <button class="incident-row" onclick="loadIncidentDetail('${i.id}')">
      <div class="incident-main">
        <strong>${escapeHtml(i.title)}</strong>
        <span>${escapeHtml(i.service_name || "")} · ${escapeHtml(i.environment || "")}</span>
      </div>
      <div class="incident-meta">
        <span class="tag severity-${String(i.severity || "").toLowerCase()}">${escapeHtml(i.severity || "")}</span>
        <span class="status-tag">${escapeHtml(i.status || "")}</span>
        <small>${formatDate(i.created_at)}</small>
      </div>
    </button>`;
}

async function loadIncidentDetail(id) {
  currentIncidentId = id;
  try {
    const incident = await api(`/incidents/incidents/${id}`);
    document.getElementById("detail-title").textContent = incident.title;
    document.getElementById("incident-detail").innerHTML = `
      <div class="detail-grid">
        <div><span>ID</span><strong>${escapeHtml(incident.id)}</strong></div>
        <div><span>Service</span><strong>${escapeHtml(incident.service_name)}</strong></div>
        <div><span>Environment</span><strong>${escapeHtml(incident.environment)}</strong></div>
        <div><span>Severity</span><strong>${escapeHtml(incident.severity)}</strong></div>
        <div><span>Status</span><strong>${escapeHtml(incident.status)}</strong></div>
        <div><span>Created</span><strong>${formatDate(incident.created_at)}</strong></div>
      </div>
      <div class="description-box"><span>Description</span><p>${escapeHtml(incident.description)}</p></div>`;
    document.getElementById("update-status").value = "";
    document.getElementById("update-severity").value = "";
    document.getElementById("assigned-engineer").value = "";
    await Promise.all([loadSavedAnalysis(), loadDetailTimeline(), loadDetailAudit()]);
    showPage("incident-detail");
  } catch (e) {
    toast(e.message, true);
  }
}

async function updateIncident() {
  if (!currentIncidentId) return;
  const body = {};
  const status = document.getElementById("update-status").value;
  const severity = document.getElementById("update-severity").value;
  const assigned_engineer = document.getElementById("assigned-engineer").value.trim();
  if (status) body.status = status;
  if (severity) body.severity = severity;
  if (assigned_engineer) body.assigned_engineer = assigned_engineer;
  if (!Object.keys(body).length) return toast("Choose a change first.", true);

  try {
    await api(`/incidents/incidents/${currentIncidentId}`, {
      method: "PATCH",
      body: JSON.stringify(body)
    });
    toast("Incident updated.");
    await loadIncidentDetail(currentIncidentId);
  } catch (e) {
    toast(e.message, true);
  }
}

async function uploadLog() {
  const file = document.getElementById("log-file").files[0];
  const source = document.getElementById("log-source").value;
  if (!file) return setMessage("log-message", "Select a log file first.", true);
  if (!currentIncidentId) return setMessage("log-message", "Select an incident first.", true);

  const form = new FormData();
  form.append("file", file);
  form.append("incident_id", currentIncidentId);
  form.append("source", source);

  try {
    await api("/logs/logs/upload", {method: "POST", body: form});
    setMessage("log-message", "Log uploaded successfully.", false);
    await loadDetailTimeline();
  } catch (e) {
    setMessage("log-message", e.message, true);
  }
}

async function analyzeIncident() {
  if (!currentIncidentId) return;
  const empty = document.getElementById("analysis-empty");
  empty.textContent = "Analyzing incident...";
  try {
    const analysis = await api(`/analysis/analysis/${currentIncidentId}`, {method: "POST"});
    renderAnalysis(analysis);
    await loadDetailTimeline();
    toast("AI analysis generated.");
  } catch (e) {
    empty.textContent = `Analysis failed: ${e.message}`;
    toast(e.message, true);
  }
}

async function loadSavedAnalysis() {
  const result = document.getElementById("analysis-result");
  const empty = document.getElementById("analysis-empty");
  try {
    const analysis = await api(`/analysis/analysis/${currentIncidentId}`);
    renderAnalysis(analysis);
  } catch {
    result.classList.add("hidden");
    empty.classList.remove("hidden");
    empty.textContent = "No saved analysis yet. Run AI analysis to generate one.";
  }
}

function renderAnalysis(a) {
  document.getElementById("analysis-empty").classList.add("hidden");
  const result = document.getElementById("analysis-result");
  result.classList.remove("hidden");
  document.getElementById("analysis-model").textContent = a.model_used || "";
  const fields = [
    ["Executive Summary", a.executive_summary],
    ["Summary", a.summary],
    ["Root Cause", a.root_cause],
    ["Business Impact", a.business_impact],
    ["Immediate Actions", a.immediate_actions],
    ["Suggested Fix", a.suggested_fix],
    ["Prevention", a.prevention],
    ["Follow-up Actions", a.follow_up_actions],
    ["Operational Runbook", a.runbook],
    ["Risk If Ignored", a.risk_if_ignored],
    ["Confidence Reason", a.confidence_reason]
  ];
  result.innerHTML = `
    <div class="metrics-grid analysis-metrics">
      <div class="metric-card"><span>Confidence</span><strong>${a.confidence ?? 0}%</strong></div>
      <div class="metric-card"><span>Priority</span><strong>${escapeHtml(a.priority || "-")}</strong></div>
      <div class="metric-card"><span>Category</span><strong>${escapeHtml(a.category || "-")}</strong></div>
      <div class="metric-card"><span>Subcategory</span><strong>${escapeHtml(a.subcategory || "-")}</strong></div>
      <div class="metric-card"><span>Affected component</span><strong>${escapeHtml(a.affected_component || "-")}</strong></div>
      <div class="metric-card"><span>Severity prediction</span><strong>${escapeHtml(a.severity_prediction || "-")}</strong></div>
      <div class="metric-card"><span>Similar incidents</span><strong>${a.retrieved_count ?? 0}</strong></div>
    </div>
    ${fields.map(([title, value]) => `<div class="analysis-block"><h4>${escapeHtml(title)}</h4><p>${escapeHtml(value || "—")}</p></div>`).join("")}
    <div class="analysis-block"><h4>Retrieved incidents</h4><p>${(a.retrieved_incidents || []).map(escapeHtml).join(", ") || "None"}</p></div>`;
}

async function loadDetailTimeline() {
  try {
    const events = await api(`/timeline/timeline/${currentIncidentId}`);
    document.getElementById("detail-timeline").innerHTML =
      (events || []).map(renderTimelineEvent).join("") || `<div class="empty">No timeline events.</div>`;
  } catch (e) {
    document.getElementById("detail-timeline").innerHTML = `<div class="empty">${escapeHtml(e.message)}</div>`;
  }
}

function renderTimelineEvent(e) {
  return `<div class="timeline-event"><div class="timeline-dot"></div><div><strong>${escapeHtml(e.event_type)}</strong><p>${escapeHtml(e.description)}</p><small>${formatDate(e.created_at)}</small></div></div>`;
}

async function loadDetailAudit() {
  try {
    const logs = await api(`/audit/incidents/${currentIncidentId}/audit`);
    document.getElementById("detail-audit").innerHTML =
      (logs || []).map(renderAudit).join("") || `<div class="empty">No audit entries.</div>`;
  } catch (e) {
    document.getElementById("detail-audit").innerHTML = `<div class="empty">${escapeHtml(e.message)}</div>`;
  }
}

function renderAudit(a) {
  return `<div class="audit-row"><strong>${escapeHtml(a.action)}</strong><span>${escapeHtml(a.old_value || "—")} → ${escapeHtml(a.new_value || "—")}</span><small>${formatDate(a.created_at)}</small></div>`;
}

async function populateIncidentSelectors() {
  if (!cachedIncidents.length) {
    try {
      const data = await api(`/incidents/incidents?page=1&limit=100`);
      cachedIncidents = Array.isArray(data) ? data : (data?.items || data?.incidents || []);
    } catch { return; }
  }
  const options = `<option value="">Select incident</option>` +
    cachedIncidents.map(i => `<option value="${i.id}">${escapeHtml(i.title)}</option>`).join("");
  document.getElementById("timeline-incident").innerHTML = options;
  document.getElementById("audit-incident").innerHTML = options;
}

async function loadTimeline() {
  const id = document.getElementById("timeline-incident").value;
  const target = document.getElementById("timeline-list");
  if (!id) return target.innerHTML = `<div class="empty">Select an incident.</div>`;
  try {
    const events = await api(`/timeline/timeline/${id}`);
    target.innerHTML = (events || []).map(renderTimelineEvent).join("") || `<div class="empty">No timeline events.</div>`;
  } catch (e) {
    target.innerHTML = `<div class="empty">${escapeHtml(e.message)}</div>`;
  }
}

async function loadAudit() {
  const id = document.getElementById("audit-incident").value;
  const target = document.getElementById("audit-list");
  if (!id) return target.innerHTML = `<div class="empty">Select an incident.</div>`;
  try {
    const logs = await api(`/audit/incidents/${id}/audit`);
    target.innerHTML = (logs || []).map(renderAudit).join("") || `<div class="empty">No audit entries.</div>`;
  } catch (e) {
    target.innerHTML = `<div class="empty">${escapeHtml(e.message)}</div>`;
  }
}

async function sendChat() {
  const input = document.getElementById("chat-question");
  const question = input.value.trim();
  if (!question) return;
  addChat("user", question);
  input.value = "";
  try {
    const response = await api("/ai/chat", {
      method: "POST",
      body: JSON.stringify({
        task: "chat",
        question: question
    })
    });
    addChat("assistant", response.answer || response.response || "No answer returned.");
  } catch (e) {
    addChat("assistant", `Error: ${e.message}`);
  }
}

function addChat(role, text) {
    const box = document.getElementById("chat-messages");
    const div = document.createElement("div");

    div.className = `chat-message ${role}`;

    // Escape HTML so AI responses cannot inject HTML/JavaScript
    const safeText = String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    // Convert only the Markdown formatting we want to support
    const formattedText = safeText
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n/g, "<br>");

    div.innerHTML = formattedText;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

function setMessage(id, text, error) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.className = `message ${error ? "error" : "success"}`;
}

function toast(text, error = false) {
  const el = document.getElementById("toast");
  el.textContent = text;
  el.className = `toast ${error ? "error" : ""}`;
  setTimeout(() => el.classList.add("hidden"), 3500);
}

function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleString();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

document.getElementById("chat-question")?.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendChat();
  }
});

if (getToken()) {
  startApp();
}
