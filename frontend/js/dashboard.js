import { ensureAuthenticated } from "./authGuard.js";
import {
    loadMetrics,
    loadActivity,
    loadAnnouncements,
    loadCategories,
    loadAnalyticsChart
} from "./dashboardLoaders.js";

ensureAuthenticated();

loadMetrics();
loadActivity();
loadAnnouncements();
loadCategories();
loadAnalyticsChart();

// Sidebar toggle from your HTML
const sidebar = document.getElementById("sidebar");
document.getElementById("sidebarToggle").addEventListener("click", () => {
    sidebar.classList.toggle("show");
});


