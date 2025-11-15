import {
    getMetrics,
    getActivity,
    getAnnouncements,
    getCategories,
    getAnalytics,
    getBookmarks,
    getNotes
} from "./api.js";


// 1. METRICS (cards at the top)
export async function loadMetrics() {
    const data = await getMetrics();

    document.getElementById("totalNotes").innerText = data.total_notes;
    document.getElementById("totalBookmarks").innerText = data.total_bookmarks;
    document.getElementById("totalCategories").innerText = data.total_categories;
    document.getElementById("lastSynced").innerText = data.last_synced;
}


// 2. ACTIVITY FEED
export async function loadActivity() {
    const list = document.getElementById("activityList");
    const data = await getActivity();

    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerText = `${item.description} – ${item.timestamp}`;
        list.appendChild(li);
    });
}


// 3. ANNOUNCEMENTS
export async function loadAnnouncements() {
    const container = document.getElementById("announcementsBox");
    const data = await getAnnouncements();

    container.innerHTML = "";

    data.forEach(a => {
        container.innerHTML += `
            <div class="alert alert-info mb-2">
                <strong>${a.title}</strong><br>
                <small>${a.date}</small>
                <p class="mb-0">${a.message}</p>
            </div>
        `;
    });
}


// 4. CATEGORIES (for filters and modal forms)
export async function loadCategories() {
    const select = document.getElementById("categoryFilter");
    const modalSelect = document.getElementById("noteCategory");

    const data = await getCategories();

    select.innerHTML = `<option value="all">All Categories</option>`;
    modalSelect.innerHTML = "";

    data.forEach(cat => {
        select.innerHTML += `<option value="${cat.id}">${cat.name}</option>`;
        modalSelect.innerHTML += `<option value="${cat.id}">${cat.name}</option>`;
    });
}


// 5. ANALYTICS CHART (Chart.js)
export async function loadAnalyticsChart() {
    const ctx = document.getElementById("notesChart");

    if (!ctx) return;

    const data = await getAnalytics();

    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: "Bookmarks",
                data: data.bookmarks,
                backgroundColor: "rgba(13,110,253,0.3)",
                borderColor: "rgb(13,110,253)",
                borderWidth: 2,
                tension: 0.3
            },
            {
                label: "Notes",
                data: data.notes,
                backgroundColor: "rgba(25,135,84,0.3)",
                borderColor: "rgb(25,135,84)",
                borderWidth: 2,
                tension: 0.3
            }
        ]
    };

    new Chart(ctx, {
        type: "line",
        data: chartData,
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}
