// base.js - Utility script for admin panel base layout
// The logout link in sidebar uses regular <a> navigation to /admin/logout
// which clears the session and redirects to the homepage.
// No additional JS handling is required.

document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logout-button"); // Sesuaikan id tombol logout di HTML kamu
    
    if (logoutBtn) {
        logoutBtn.addEventListener("click", async function (e) {
            e.preventDefault();
            
            if (confirm("Apakah Anda yakin ingin keluar dari Admin Panel?")) {
                try {
                    const response = await fetch('/admin/logout', {
                        headers: { 'Accept': 'application/json' }
                    });
                    const result = await response.json();
                    
                    if (result.success) {
                        alert("Anda telah logout.");
                        window.location.href = result.redirect; // Diarahkan ke /admin/login
                    }
                } catch (error) {
                    console.error("Gagal melakukan logout:", error);
                    alert("Terjadi kesalahan sistem.");
                }
            }
        });
    }
});