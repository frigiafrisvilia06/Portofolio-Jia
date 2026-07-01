document.addEventListener("DOMContentLoaded", function () {
    const formProyek = document.getElementById("form-proyek-admin");
    const projListContainer = document.getElementById("projects-list-container");
    const projectIdInput = document.getElementById("project-id");
    const existingGambarUrl = document.getElementById("existing-gambar-url");
    const btnCancel = document.getElementById("btn-cancel");
    const formTitle = document.getElementById("form-title");

    // 1. Ambil List Data saat Halaman Dibuka
    loadProjects();

    function loadProjects() {
        fetch('/admin/api/projects')
            .then(res => res.json())
            .then(data => {
                projListContainer.innerHTML = "";
                if (!data || data.length === 0) {
                    projListContainer.innerHTML = `<p style="color:gray;">Belum ada proyek di database.</p>`;
                    return;
                }
                data.forEach(proj => {
                    const id = proj.id;
                    const judul = proj.judul_proyek || "";
                    const deskripsi = proj.deskripsi || "";
                    const link = proj.link_proyek || "";
                    const fotoUrl = proj.gambar_url || 'https://via.placeholder.com/300x160?text=No+Image';

                    const card = document.createElement("div");
                    card.style.cssText = "background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.01);";
                    card.innerHTML = `
                        <img src="${fotoUrl}" style="width: 100%; height: 160px; object-fit: cover;">
                        <div style="padding: 15px;">
                            <h4 style="font-weight: 700; font-size: 16px; margin-bottom: 8px;">${judul}</h4>
                            <p style="color: #666; font-size: 13px; margin-bottom: 12px; height: 40px; overflow: hidden;">${deskripsi}</p>
                            <a href="${link}" target="_blank" style="font-size: 12px; color: #0066cc; display: block; margin-bottom: 12px; text-decoration: none;"><i class="fas fa-external-link-alt"></i> Lihat Demo</a>
                            <div style="display: flex; gap: 8px;">
                                <button class="btn-edit" data-id="${id}" data-judul="${judul}" data-deskripsi="${deskripsi}" data-link="${link}" data-foto="${fotoUrl}" style="flex:1; background: #ffc107; border: none; color: #fff; padding: 6px; border-radius: 6px; font-weight:600; cursor: pointer; font-size: 11px;"><i class="fas fa-edit"></i> Edit</button>
                                <button class="btn-delete" data-id="${id}" style="flex:1; background: #dc3545; border: none; color: #fff; padding: 6px; border-radius: 6px; font-weight:600; cursor: pointer; font-size: 11px;"><i class="fas fa-trash"></i> Hapus</button>
                            </div>
                        </div>
                    `;
                    projListContainer.appendChild(card);
                });
                initActionButtons();
            })
            .catch(err => {
                console.error("Gagal memuat proyek:", err);
                projListContainer.innerHTML = `<p style="color:red;">Gagal memuat data proyek dari server.</p>`;
            });
    }

    // 2. Event Listener Tombol Aksi (Edit & Delete)
    function initActionButtons() {
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", function(e) {
                const target = e.target.closest('.btn-edit');
                if (!target) return;
                formTitle.innerText = "Ubah Data Proyek";
                projectIdInput.value = target.dataset.id;
                document.getElementById("admin-judul-proyek").value = target.dataset.judul;
                document.getElementById("admin-deskripsi-proyek").value = target.dataset.deskripsi;
                document.getElementById("admin-link-proyek").value = target.dataset.link;
                existingGambarUrl.value = target.dataset.foto; // Simpan URL gambar lama jika tidak diganti
                btnCancel.style.display = "inline-block";
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });

        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", function(e) {
                const target = e.target.closest('.btn-delete');
                if (!target) return;
                if(confirm("Apakah Anda yakin menghapus proyek ini?")) {
                    fetch(`/admin/api/projects/${target.dataset.id}`, { method: "DELETE" })
                        .then(res => res.json())
                        .then(result => {
                            if (result.success) {
                                loadProjects();
                            } else {
                                alert("Gagal menghapus: " + result.message);
                            }
                        })
                        .catch(err => {
                            console.error(err);
                            alert("Terjadi kesalahan koneksi saat menghapus.");
                        });
                }
            });
        });
    }

    // 3. Modifikasi Logika Submit Asli Anda (Mendukung POST & PUT)
    if (formProyek) {
        formProyek.addEventListener("submit", async function (e) {
            e.preventDefault();

            const id = projectIdInput.value;
            const fileInput = document.getElementById("input-file-gambar");
            let secureUrlGambar = id ? existingGambarUrl.value : ""; // Gunakan gambar lama jika mode edit dan tidak ganti gambar

            // Jika memilih berkas baru, lakukan upload ke Cloudinary terlebih dahulu
            if (fileInput.files.length > 0) {
                const formData = new FormData();
                formData.append("file", fileInput.files[0]);

                try {
                    // Penyesuaian path route blueprint admin
                    const uploadResponse = await fetch('/admin/api/upload', {
                        method: 'POST',
                        body: formData
                    });
                    const uploadResult = await uploadResponse.json();
                    
                    if (uploadResult.secure_url) {
                        secureUrlGambar = uploadResult.secure_url;
                    } else {
                        alert("Gagal mengunggah gambar ke Cloudinary.");
                        return;
                    }
                } catch (err) {
                    console.error("Error upload gambar:", err);
                    return;
                }
            }

            // Gabung data teks & URL gambar Cloudinary
            const dataProyek = {
                judul_proyek: document.getElementById("admin-judul-proyek").value,
                deskripsi: document.getElementById("admin-deskripsi-proyek").value,
                link_proyek: document.getElementById("admin-link-proyek").value,
                gambar_url: secureUrlGambar
            };

            const url = id ? `/admin/api/projects/${id}` : '/admin/api/projects';
            const method = id ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataProyek)
            });

            const result = await response.json();
            if (result.success) {
                alert(id ? "Proyek berhasil diperbarui!" : "Proyek baru berhasil disimpan!");
                resetForm();
                loadProjects();
            }
        });
    }

    btnCancel.addEventListener("click", resetForm);

    function resetForm() {
        formTitle.innerText = "Tambah / Edit Proyek";
        projectIdInput.value = "";
        existingGambarUrl.value = "";
        formProyek.reset();
        btnCancel.style.display = "none";
    }
});