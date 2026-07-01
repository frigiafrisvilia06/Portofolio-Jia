// Frontend/utama/js/script.js

document.addEventListener("DOMContentLoaded", function () {
    muatDataPortofolio();
    setupFormKontak();
});

// 1. Ambil data dari backend dan suntikkan ke elemen HTML halaman utama
async function muatDataPortofolio() {
    try {
        const response = await fetch('/api/portfolio-data');
        const data = await response.json();

        // Render Data Profil
        if (data.profil) {
            document.getElementById("nama-anda").innerText = data.profil.nama;
            document.getElementById("peran-anda").innerText = data.profil.peran;
            document.getElementById("deskripsi-anda").innerText = data.profil.deskripsi;
            if (data.profil.foto_url) {
                document.getElementById("foto-anda").src = data.profil.foto_url;
            }
        }

        // Render Data Keahlian (Skills)
        const gridSkill = document.getElementById("skills-container");
        if (gridSkill && data.skills) {
            gridSkill.innerHTML = "";
            data.skills.forEach(skill => {
                gridSkill.innerHTML += `
                    <div class="skill-card">
                        <h4>${skill.nama_skill}</h4>
                        <span>${skill.kategori}</span>
                    </div>`;
            });
        }

        // Render Data Pengalaman (Timeline)
        const timeline = document.getElementById("timeline-container");
        if (timeline && data.pengalaman) {
            timeline.innerHTML = "";
            data.pengalaman.forEach(exp => {
                timeline.innerHTML += `
                    <div class="timeline-item">
                        <h3>${exp.posisi}</h3>
                        <h5>${exp.perusahaan_organisasi}</h5>
                        <small>${exp.tanggal_mulai} - ${exp.tanggal_selesai}</small>
                        <p>${exp.deskripsi}</p>
                    </div>`;
            });
        }

        // Render Data Proyek
        const gridProyek = document.getElementById("projects-grid");
        if (gridProyek && data.projects) {
            gridProyek.innerHTML = "";
            data.projects.forEach(proj => {
                gridProyek.innerHTML += `
                    <div class="project-card">
                        <img src="${proj.gambar_url || 'https://via.placeholder.com/300'}" alt="${proj.judul_proyek}">
                        <h3>${proj.judul_proyek}</h3>
                        <p>${proj.deskripsi}</p>
                        <a href="${proj.link_proyek}" target="_blank" class="btn">Lihat Proyek</a>
                    </div>`;
            });
        }
    } catch (error) {
        console.error("Gagal memuat data utama:", error);
    }
}

// 2. Kirim Pesan Kontak -> Masuk TiDB & Tembak Notifikasi ke Resend Email
function setupFormKontak() {
    const form = document.getElementById("form-kontak-utama");
    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const payload = {
            nama_pengirim: document.getElementById("input-nama").value,
            email_pengirim: document.getElementById("input-email").value,
            pesan: document.getElementById("textarea-pesan").value
        };

        try {
            const response = await fetch('/api/kontak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await response.json();

            if (result.success) {
                alert("Pesan sukses dikirim! Salinan notifikasi dikirim via Resend.");
                form.reset();
            } else {
                alert("Gagal mengirim pesan: " + result.message);
            }
        } catch (error) {
            console.error("Gagal kontak:", error);
        }
    });
}