from flask import Blueprint, request, jsonify, render_template, current_app
from Backend.admin.login import login_required

# Nama blueprint disesuaikan dengan registrasi di app.py
experience_bp = Blueprint('experience_admin', __name__)

# 1. Menampilkan Halaman Experience
@experience_bp.route('/experience')
@login_required
def experience_page():
    return render_template('Frontend/admin/experience.html')


# 2. API Handle GET (Read) & POST (Create)
@experience_bp.route('/api/experience', methods=['GET', 'POST'])
@login_required
def handle_experience():
    db = current_app.get_db()
    
    if request.method == 'POST':
        data = request.get_json()
        perusahaan = data.get('perusahaan_organisasi')
        posisi = data.get('posisi')
        tgl_mulai = data.get('tanggal_mulai')
        tgl_selesai = data.get('tanggal_selesai')
        deskripsi = data.get('deskripsi')
        
        if not perusahaan or not posisi:
            return jsonify({"success": False, "message": "Perusahaan dan posisi wajib diisi"}), 400
            
        try:
            with db.cursor() as cursor:
                sql = """
                    INSERT INTO pengalaman (perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (perusahaan, posisi, tgl_mulai, tgl_selesai, deskripsi))
                db.commit()
            return jsonify({"success": True, "message": "Pengalaman berhasil ditambahkan ke TiDB!"}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Gagal menyimpan data: {str(e)}"}), 500
            
    # GET Request: Ambil semua pengalaman
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id, perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi FROM pengalaman ORDER BY id DESC")
            all_experience = cursor.fetchall()
        return jsonify(all_experience)
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil data: {str(e)}"}), 500


# 3. API Handle PUT (Update)
@experience_bp.route('/api/experience/<int:id>', methods=['PUT'])
@login_required
def update_experience(id):
    db = current_app.get_db()
    data = request.get_json()
    perusahaan = data.get('perusahaan_organisasi')
    posisi = data.get('posisi')
    tgl_mulai = data.get('tanggal_mulai')
    tgl_selesai = data.get('tanggal_selesai')
    deskripsi = data.get('deskripsi')
    
    if not perusahaan or not posisi:
        return jsonify({"success": False, "message": "Perusahaan dan posisi wajib diisi"}), 400
        
    try:
        with db.cursor() as cursor:
            sql = """
                UPDATE pengalaman 
                SET perusahaan_organisasi = %s, posisi = %s, tanggal_mulai = %s, tanggal_selesai = %s, deskripsi = %s 
                WHERE id = %s
            """
            cursor.execute(sql, (perusahaan, posisi, tgl_mulai, tgl_selesai, deskripsi, id))
            db.commit()
        return jsonify({"success": True, "message": "Pengalaman berhasil diperbarui di TiDB!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal memperbarui data: {str(e)}"}), 500


# 4. API Handle DELETE (Hapus)
@experience_bp.route('/api/experience/<int:id>', methods=['DELETE'])
@login_required
def delete_experience(id):
    db = current_app.get_db()
    
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM pengalaman WHERE id = %s"
            cursor.execute(sql, (id,))
            db.commit()
        return jsonify({"success": True, "message": "Pengalaman berhasil dihapus dari TiDB!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal menghapus data: {str(e)}"}), 500