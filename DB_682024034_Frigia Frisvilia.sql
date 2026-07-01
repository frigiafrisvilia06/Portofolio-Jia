CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE profil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_lengkap VARCHAR(100) NOT NULL,
    nama_panggilan VARCHAR(50),
    peran VARCHAR(100),          -- Contoh: Backend Developer & Python Enthusiast
    deskripsi TEXT,               -- Bio/deskripsi singkat untuk halaman portofolio
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    email VARCHAR(100),
    telepon VARCHAR(20),
    universitas VARCHAR(100),
    fakultas VARCHAR(100),
    prodi VARCHAR(100),
    semester INT,
    alamat TEXT,
    avatar_url VARCHAR(255) -- Untuk menyimpan secure_url dari Cloudinary
);

CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_skill VARCHAR(50) NOT NULL,
    kategori VARCHAR(50), -- Contoh: Frontend, Backend, Mobile
    tingkat VARCHAR(30)   -- Contoh: Beginner, Advance, Expert (Opsional)
);

CREATE TABLE pengalaman (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perusahaan_organisasi VARCHAR(100) NOT NULL,
    posisi VARCHAR(100) NOT NULL,
    tanggal_mulai VARCHAR(50),
    tanggal_selesai VARCHAR(50),
    deskripsi TEXT
);

CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul_proyek VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    link_proyek VARCHAR(255),
    gambar_url VARCHAR(255) -- Untuk menyimpan secure_url dari Cloudinary
);

CREATE TABLE kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pengirim VARCHAR(100) NOT NULL,
    email_pengirim VARCHAR(100) NOT NULL,
    pesan TEXT NOT NULL,
    tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default data untuk login admin awal
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

-- Default baris profil agar bisa di-UPDATE langsung di form akun pertama kali
INSERT INTO profil (nama_lengkap, email) VALUES ('Nama Admin', 'admin@email.com');