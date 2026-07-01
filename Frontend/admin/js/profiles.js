document.addEventListener("DOMContentLoaded", function () {
    const formDiri = document.getElementById("form-data-diri");
    const formPass = document.getElementById("form-ubah-password");
    let currentExistingAvatar = "";

    // Load Data Awal
    loadProfileData();

    async function loadProfileData() {
        try {
            const res = await fetch('/admin/api/profile');
            const data = await res.json();
            
            if(data) {
                // Populate input form
                document.getElementById("nama-lengkap").value = data.nama_lengkap || "";
                document.getElementById("nama-panggilan").value = data.nama_panggilan || "";
                document.getElementById("profile-peran").value = data.peran || "";
                document.getElementById("profile-deskripsi").value = data.deskripsi || "";
                document.getElementById("tempat-lahir").value = data.tempat_lahir || "";
                document.getElementById("tanggal-lahir").value = data.tanggal_lahir || "";
                document.getElementById("profile-email").value = data.email || "";
                document.getElementById("profile-telepon").value = data.telepon || "";
                document.getElementById("profile-universitas").value = data.universitas || "";
                document.getElementById("profile-fakultas").value = data.fakultas || "";
                document.getElementById("profile-prodi").value = data.prodi || "";
                document.getElementById("profile-semester").value = data.semester || "";
                document.getElementById("profile-alamat").value = data.alamat || "";
                
                currentExistingAvatar = data.avatar_url || "";

                // Populate live preview area
                document.getElementById("view-nama").innerText = data.nama_lengkap || "-";
                document.getElementById("view-panggilan").innerText = data.nama_panggilan || "-";
                document.getElementById("view-ttl").innerText = `${data.tempat_lahir || ''}, ${data.tanggal_lahir || ''}`;
                document.getElementById("view-email").innerText = data.email || "-";
                document.getElementById("view-telepon").innerText = data.telepon || "-";
                document.getElementById("view-universitas").innerText = data.universitas || "-";
                document.getElementById("view-fakultas").innerText = data.fakultas || "-";
                
                if (data.avatar_url) {
                    document.getElementById("preview-avatar").src = data.avatar_url;
                }
            }
        } catch (err) { console.error("Gagal memuat profil:", err); }
    }

    // SIMPAN DATA DIRI (Dengan Upload Dua Tahap ala Anda)
    formDiri.addEventListener("submit", async function (e) {
        e.preventDefault();
        const fileInput = document.getElementById("input-avatar-profil");
        let finalAvatarUrl = currentExistingAvatar;

        if (fileInput.files.length > 0) {
            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            try {
                const uploadResponse = await fetch('/admin/api/upload', { method: 'POST', body: formData });
                const uploadResult = await uploadResponse.json();
                if (uploadResult.secure_url) {
                    finalAvatarUrl = uploadResult.secure_url;
                } else {
                    alert("Gagal mengunggah avatar.");
                    return;
                }
            } catch (err) { return; }
        }

        const payload = {
            nama_lengkap: document.getElementById("nama-lengkap").value,
            nama_panggilan: document.getElementById("nama-panggilan").value,
            peran: document.getElementById("profile-peran").value,
            deskripsi: document.getElementById("profile-deskripsi").value,
            tempat_lahir: document.getElementById("tempat-lahir").value,
            tanggal_lahir: document.getElementById("tanggal-lahir").value,
            email: document.getElementById("profile-email").value,
            telepon: document.getElementById("profile-telepon").value,
            universitas: document.getElementById("profile-universitas").value,
            fakultas: document.getElementById("profile-fakultas").value,
            prodi: document.getElementById("profile-prodi").value,
            semester: document.getElementById("profile-semester").value,
            alamat: document.getElementById("profile-alamat").value,
            avatar_url: finalAvatarUrl
        };

        const response = await fetch('/admin/api/profile', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if(result.success) {
            alert("Profil Anda berhasil diperbarui di TiDB!");
            loadProfileData();
        }
    });

    // UBAH PASSWORD
    formPass.addEventListener("submit", async function (e) {
        e.preventDefault();
        const curPass = document.getElementById("pass-current").value;
        const newPass = document.getElementById("pass-new").value;
        const confPass = document.getElementById("pass-confirm").value;

        if(newPass !== confPass) {
            alert("Konfirmasi password baru tidak cocok!");
            return;
        }

        const response = await fetch('/admin/api/change-password', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ current_password: curPass, new_password: newPass })
        });

        const result = await response.json();
        if(result.success) {
            alert("Password berhasil diubah!");
            formPass.reset();
        } else {
            alert("Gagal: " + result.message);
        }
    });
});