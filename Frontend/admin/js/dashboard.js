// Frontend/admin/js/dashboard.js

document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch('/admin/api/admin/stats');
        const result = await response.json();

        if (result.success) {
            // Pasang angka ke kotak dashboard sesuai id di HTML
            document.getElementById("count-skills").innerText = result.stats.skills;
            document.getElementById("count-experience").innerText = result.stats.experience;
            document.getElementById("count-projects").innerText = result.stats.projects;
        }
    } catch (error) {
        console.error("Gagal memuat summary dashboard:", error);
    }
});
