document.addEventListener("DOMContentLoaded", function () {
    const formExp = document.getElementById("form-experience");
    const expListContainer = document.getElementById("experience-list-container");
    const expIdInput = document.getElementById("experience-id");
    const tanggalMulaiInput = document.getElementById("tanggal_mulai");
    const tanggalSelesaiInput = document.getElementById("tanggal_selesai");
    const posisiInput = document.getElementById("posisi");
    const perusahaanOrganisasiInput = document.getElementById("perusahaan_organisasi");
    const deskripsiInput = document.getElementById("deskripsi");
    const formTitle = document.getElementById("form-title");
    const btnCancel = document.getElementById("btn-cancel");

    loadExperiences();

    // 1. Ambil Data (GET) & Render Kartu Lebar
    function loadExperiences() {
        fetch('/admin/api/experience')
            .then(res => res.json())
            .then(data => {
                expListContainer.innerHTML = "";
                if (!data || data.length === 0) {
                    expListContainer.innerHTML = `<p style="color:gray; padding:10px;">Belum ada riwayat pengalaman.</p>`;
                    return;
                }
                
                data.forEach(exp => {
                    // Penyesuaian ke format dictionary dari DictCursor
                    const id = exp.id;
                    const tanggalMulai = exp.tanggal_mulai || "";
                    const tanggalSelesai = exp.tanggal_selesai || "Sekarang";
                    const posisi = exp.posisi || "";
                    const perusahaan = exp.perusahaan_organisasi || "";
                    const deskripsi = exp.deskripsi || "";

                    const card = document.createElement("div");
                    card.style.cssText = "background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; max-width: 450px; box-shadow: 0 2px 4px rgba(0,0,0,0.01); display: flex; flex-direction: column; gap: 12px;";
                    
                    card.innerHTML = `
                        <div>
                            <h4 style="font-weight: 700; font-size: 16px; margin-bottom: 4px; color: #333;">${posisi}</h4>
                            <p style="color: #888; font-size: 13px; margin-bottom: 8px;">${perusahaan} | ${tanggalMulai} - ${tanggalSelesai}</p>
                            <p style="color: #555; font-size: 14px; line-height: 1.5; white-space: pre-line;">${deskripsi}</p>
                        </div>
                        
                        <div style="display: flex; gap: 8px; margin-top: 5px;">
                            <button class="btn-edit" data-id="${id}" data-tanggal_mulai="${tanggalMulai}" data-tanggal_selesai="${tanggalSelesai}" data-posisi="${posisi}" data-perusahaan_organisasi="${perusahaan}" data-deskripsi="${deskripsi}" style="background: #ffc107; border: none; color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight:600; cursor: pointer;"><i class="fas fa-edit"></i> Edit</button>
                            <button class="btn-delete" data-id="${id}" style="background: #dc3545; border: none; color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight:600; cursor: pointer;"><i class="fas fa-trash"></i> Hapus</button>
                        </div>
                    `;
                    expListContainer.appendChild(card);
                });

                initActionButtons();
            })
            .catch(err => {
                console.error("Gagal memuat pengalaman:", err);
                expListContainer.innerHTML = `<p style="color:red; padding:10px;">Gagal memuat data pengalaman dari server.</p>`;
            });
    }

    // 2. Pasang Event Klik Edit & Delete
    function initActionButtons() {
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", function (e) {
                const target = e.target.closest('.btn-edit');
                if (!target) return;
                formTitle.innerText = "Ubah Data Pengalaman";
                expIdInput.value = target.getAttribute("data-id");
                tanggalMulaiInput.value = target.getAttribute("data-tanggal_mulai");
                const tglSelesaiVal = target.getAttribute("data-tanggal_selesai");
                tanggalSelesaiInput.value = (tglSelesaiVal === 'Sekarang' || tglSelesaiVal === 'null') ? '' : tglSelesaiVal;
                posisiInput.value = target.getAttribute("data-posisi");
                perusahaanOrganisasiInput.value = target.getAttribute("data-perusahaan_organisasi");
                deskripsiInput.value = target.getAttribute("data-deskripsi");
                btnCancel.style.display = "inline-block";
            });
        });

        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", function (e) {
                const target = e.target.closest('.btn-delete');
                if (!target) return;
                const id = target.getAttribute("data-id");
                if (confirm("Apakah Anda yakin ingin menghapus pengalaman ini?")) {
                    fetch(`/admin/api/experience/${id}`, { method: "DELETE" })
                        .then(res => res.json())
                        .then(result => {
                            if (result.success) {
                                loadExperiences();
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

    // 3. Simpan / Pembaruan Data (POST / PUT)
    formExp.addEventListener("submit", function (e) {
        e.preventDefault();
        const id = expIdInput.value;
        const payload = {
            tanggal_mulai: tanggalMulaiInput.value,
            tanggal_selesai: tanggalSelesaiInput.value || null,
            posisi: posisiInput.value,
            perusahaan_organisasi: perusahaanOrganisasiInput.value,
            deskripsi: deskripsiInput.value
        };

        const url = id ? `/admin/api/experience/${id}` : '/admin/api/experience';
        const method = id ? "PUT" : "POST";

        fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(result => {
            if (result.success) {
                alert(id ? "Pengalaman berhasil diperbarui!" : "Pengalaman baru berhasil ditambahkan!");
                resetForm();
                loadExperiences();
            } else {
                alert("Gagal menyimpan data: " + result.message);
            }
        })
        .catch(err => {
            console.error(err);
            alert("Terjadi kesalahan koneksi.");
        });
    });

    btnCancel.addEventListener("click", resetForm);

    function resetForm() {
        formTitle.innerText = "Tambah / Edit Pengalaman";
        expIdInput.value = "";
        formExp.reset();
        btnCancel.style.display = "none";
    }
});