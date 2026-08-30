const API_BASE = "http://127.0.0.1:8000";

let currentIncidentId = null;


// ==================================================
// AUTHENTICATION
// ==================================================

function getToken() {
    return localStorage.getItem("access_token");
}


function getAuthHeaders() {

    const token = getToken();

    if (!token) {
        throw new Error("Please login first.");
    }

    return {
        "Authorization": `Bearer ${token}`
    };
}


// ==================================================
// LOGIN
// ==================================================

async function login() {

    const email =
        document.getElementById("login-email").value.trim();

    const password =
        document.getElementById("login-password").value;

    const message =
        document.getElementById("login-message");


    if (!email || !password) {

        message.textContent =
            "Please enter email and password.";

        message.style.color = "red";

        return;
    }


    try {

        const response = await fetch(
            `${API_BASE}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        const data =
            await response.json();


        console.log(
            "Login successful:",
            data
        );


        // Save JWT
        localStorage.setItem(
            "access_token",
            data.access_token
        );


        message.textContent =
            "Login successful.";

        message.style.color = "green";


        // Hide login
        document
            .getElementById("login-section")
            .classList.add("hidden");


        // Show application
        document
            .getElementById("app-section")
            .classList.remove("hidden");


        // Load dashboard
        loadDashboard();

    }
    catch (error) {

        console.error(
            "Login error:",
            error
        );


        message.textContent =
            "Login failed: " +
            error.message;

        message.style.color = "red";

    }
}


// ==================================================
// LOGOUT
// ==================================================

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    currentIncidentId = null;


    document
        .getElementById("app-section")
        .classList.add("hidden");


    document
        .getElementById("login-section")
        .classList.remove("hidden");


    document.getElementById(
        "login-email"
    ).value = "";


    document.getElementById(
        "login-password"
    ).value = "";


    document.getElementById(
        "login-message"
    ).textContent = "";

}


// ==================================================
// CHECK LOGIN
// ==================================================

function checkLogin() {

    const token =
        getToken();


    if (token) {

        document
            .getElementById("login-section")
            .classList.add("hidden");


        document
            .getElementById("app-section")
            .classList.remove("hidden");


        loadDashboard();

    }

}


// ==================================================
// CREATE INCIDENT
// ==================================================

async function createIncident() {

    const title =
        document.getElementById("title").value.trim();

    const description =
        document.getElementById("description").value.trim();

    const service =
        document.getElementById("service").value.trim();

    const environment =
        document.getElementById("environment").value;

    const severity =
        document.getElementById("severity").value;

    const message =
        document.getElementById("incident-message");


    if (!title || !description || !service) {

        message.textContent =
            "Please fill in all incident fields.";

        message.style.color = "red";

        return;
    }


    try {

        const response = await fetch(
            `${API_BASE}/incidents/incidents`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    ...getAuthHeaders()
                },

                body: JSON.stringify({

                    title: title,

                    description: description,

                    service_name: service,

                    environment: environment,

                    severity: severity

                })
            }
        );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        const incident =
            await response.json();


        currentIncidentId =
            incident.id;


        document
            .getElementById("incident-section")
            .classList.remove("hidden");


        document
            .getElementById("log-section")
            .classList.remove("hidden");


        document
            .getElementById("analysis-section")
            .classList.remove("hidden");


        document.getElementById(
            "incident-id"
        ).textContent =
            incident.id;


        document.getElementById(
            "incident-title"
        ).textContent =
            incident.title;


        document.getElementById(
            "incident-service"
        ).textContent =
            incident.service_name;


        document.getElementById(
            "incident-severity"
        ).textContent =
            incident.severity;


        message.textContent =
            "Incident created successfully.";

        message.style.color = "green";


        loadDashboard();

    }
    catch (error) {

        console.error(
            "Create incident error:",
            error
        );


        message.textContent =
            "Failed to create incident: " +
            error.message;

        message.style.color = "red";

    }
}


// ==================================================
// UPLOAD LOG
// ==================================================

async function uploadLog() {

    const fileInput =
        document.getElementById("log-file");

    const message =
        document.getElementById("log-message");


    if (!currentIncidentId) {

        message.textContent =
            "Create an incident first.";

        message.style.color = "red";

        return;
    }


    if (!fileInput.files.length) {

        message.textContent =
            "Please select a log file.";

        message.style.color = "red";

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        fileInput.files[0]
    );


    formData.append(
        "incident_id",
        currentIncidentId
    );


    try {

        const response = await fetch(
            `${API_BASE}/logs/logs/upload`,
            {
                method: "POST",

                headers: {
                    ...getAuthHeaders()
                },

                body: formData
            }
        );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        message.textContent =
            "Log uploaded successfully.";

        message.style.color = "green";

    }
    catch (error) {

        console.error(
            "Upload log error:",
            error
        );


        message.textContent =
            "Failed to upload log: " +
            error.message;

        message.style.color = "red";

    }
}


// ==================================================
// AI ANALYSIS
// ==================================================

async function analyzeIncident() {

    if (!currentIncidentId) {

        alert(
            "Create an incident first."
        );

        return;
    }


    const loading =
        document.getElementById(
            "analysis-loading"
        );


    const result =
        document.getElementById(
            "analysis-result"
        );


    loading.classList.remove(
        "hidden"
    );


    result.classList.add(
        "hidden"
    );


    try {

        const response = await fetch(
            `${API_BASE}/analysis/analysis/${currentIncidentId}`,
            {
                method: "POST",

                headers: {
                    ...getAuthHeaders()
                }
            }
        );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);
        }


        const analysis =
            await response.json();


        console.log(
            "AI Analysis:",
            analysis
        );


        displayAnalysis(
            analysis
        );

    }
    catch (error) {

        console.error(
            "AI analysis error:",
            error
        );


        alert(
            "AI analysis failed.\n\n" +
            error.message
        );

    }
    finally {

        loading.classList.add(
            "hidden"
        );

    }
}


// ==================================================
// GET SAVED AI ANALYSIS
// ==================================================

async function getSavedAnalysis() {

    if (!currentIncidentId) {
        return;
    }


    try {

        const response = await fetch(
            `${API_BASE}/analysis/analysis/${currentIncidentId}`,
            {
                method: "GET",

                headers: {
                    ...getAuthHeaders()
                }
            }
        );


        if (!response.ok) {
            return;
        }


        const analysis =
            await response.json();


        displayAnalysis(
            analysis
        );

    }
    catch (error) {

        console.error(
            "Get analysis error:",
            error
        );

    }
}


// ==================================================
// DISPLAY AI ANALYSIS
// ==================================================

function displayAnalysis(analysis) {

    document
        .getElementById("analysis-result")
        .classList.remove("hidden");


    document.getElementById(
        "confidence"
    ).textContent =
        `${analysis.confidence}%`;


    document.getElementById(
        "priority"
    ).textContent =
        analysis.priority;


    document.getElementById(
        "category"
    ).textContent =
        analysis.category;


    document.getElementById(
        "retrieved-count"
    ).textContent =
        analysis.retrieved_count;


    document.getElementById(
        "executive-summary"
    ).textContent =
        analysis.executive_summary;


    document.getElementById(
        "root-cause"
    ).textContent =
        analysis.root_cause;


    document.getElementById(
        "business-impact"
    ).textContent =
        analysis.business_impact;


    document.getElementById(
        "immediate-actions"
    ).textContent =
        analysis.immediate_actions;


    document.getElementById(
        "suggested-fix"
    ).textContent =
        analysis.suggested_fix;


    document.getElementById(
        "prevention"
    ).textContent =
        analysis.prevention;


    document.getElementById(
        "follow-up-actions"
    ).textContent =
        analysis.follow_up_actions;


    document.getElementById(
        "runbook"
    ).textContent =
        analysis.runbook;


    document.getElementById(
        "risk-if-ignored"
    ).textContent =
        analysis.risk_if_ignored;


    document.getElementById(
        "confidence-reason"
    ).textContent =
        analysis.confidence_reason;

}


// ==================================================
// DASHBOARD
// ==================================================

async function loadDashboard() {

    try {

        const response = await fetch(
            `${API_BASE}/dashboard/dashboard`
        );


        if (!response.ok) {

            throw new Error(
                "Dashboard request failed"
            );

        }


        const dashboard =
            await response.json();


        document.getElementById(
            "total-incidents"
        ).textContent =
            dashboard.total_incidents;


        document.getElementById(
            "open-incidents"
        ).textContent =
            dashboard.open_incidents;


        document.getElementById(
            "resolved-incidents"
        ).textContent =
            dashboard.resolved_incidents;


        document.getElementById(
            "critical-incidents"
        ).textContent =
            dashboard.critical_incidents;


        document.getElementById(
            "high-incidents"
        ).textContent =
            dashboard.high_incidents;

    }
    catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


// ==================================================
// START APPLICATION
// ==================================================

checkLogin();