from flask import Blueprint, request, jsonify, render_template, current_app
from Backend.admin.login import login_required

profiles_bp = Blueprint('profiles_admin', __name__)

# 1. Menampilkan Halaman Akun / Profiles
@profiles_bp.route('/profiles')
@login_required
def profiles_page():
    # Diarahkan ke akun.html sesuai file template manajemen profil Anda
    return render_template('Frontend/admin/profiles.html')


# 2. API Handle GET (Read) & PUT (Update Data Diri)
@profiles_bp.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def handle_profile():
    db = current_app.get_db()
    
    if request.method == 'PUT':
        data = request.get_json()
        
        # Ambil semua field dari form Langkah 10 Anda
        nama_lengkap = data.get('nama_lengkap')
        nama_panggilan = data.get('nama_panggilan')
        tempat_lahir = data.get('tempat_lahir')
        tanggal_lahir = data.get('tanggal_lahir') # Format YYYY-MM-DD dari HTML5 input date
        email = data.get('email')
        telepon = data.get('telepon')
        universitas = data.get('universitas')
        fakultas = data.get('fakultas')
        prodi = data.get('prodi')
        semester = data.get('semester')
        alamat = data.get('alamat')
        peran = data.get('peran')
        deskripsi = data.get('deskripsi')
        avatar_url = data.get('avatar_url') # Link secure_url dari Cloudinary
        
        if not nama_lengkap:
            return jsonify({"success": False, "message": "Nama lengkap wajib diisi"}), 400
            
        try:
            with db.cursor() as cursor:
                # Periksa apakah sudah ada baris di tabel profil
                cursor.execute("SELECT COUNT(*) as total FROM profil")
                has_data = cursor.fetchone()['total'] > 0
                
                if not has_data:
                    # Jika database masih kosong (pemasangan awal), lakukan INSERT
                    sql = """
                        INSERT INTO profil (nama_lengkap, nama_panggilan, peran, deskripsi, tempat_lahir, tanggal_lahir, 
                        email, telepon, universitas, fakultas, prodi, semester, alamat, avatar_url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    params = (nama_lengkap, nama_panggilan, peran, deskripsi, tempat_lahir, tanggal_lahir, 
                              email, telepon, universitas, fakultas, prodi, semester, alamat, avatar_url)
                else:
                    # Jika sudah ada isinya, kunci pembaruan pada id = 1 (Profil Tunggal)
                    sql = """
                        UPDATE profil SET 
                            nama_lengkap = %s, nama_panggilan = %s, peran = %s, deskripsi = %s,
                            tempat_lahir = %s, tanggal_lahir = %s, 
                            email = %s, telepon = %s, universitas = %s, fakultas = %s, prodi = %s, 
                            semester = %s, alamat = %s, avatar_url = %s 
                        WHERE id = 1
                    """
                    params = (nama_lengkap, nama_panggilan, peran, deskripsi, tempat_lahir, tanggal_lahir, 
                              email, telepon, universitas, fakultas, prodi, semester, alamat, avatar_url)
                
                cursor.execute(sql, params)
                db.commit()
            return jsonify({"success": True, "message": "Data diri berhasil disimpan ke TiDB!"}), 200
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Gagal memperbarui profil: {str(e)}"}), 500

    # GET Request: Ambil data profil untuk ditampilkan di Form & Preview Live
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM profil LIMIT 1")
            profil_data = cursor.fetchone()
            
            # Jika database masih kosong, kembalikan objek kosong agar frontend tidak crash
            if not profil_data:
                return jsonify({})
                
            # Konversi format tanggal lahir ke string agar aman saat di-parse ke JSON JSON-serializable
            if profil_data.get('tanggal_lahir'):
                profil_data['tanggal_lahir'] = profil_data['tanggal_lahir'].strftime('%Y-%m-%d')
                
        return jsonify(profil_data)
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal memuat data: {str(e)}"}), 500