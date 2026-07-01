from flask import Blueprint, request, jsonify, render_template, current_app
from Backend.admin.login import login_required

# Pastikan nama blueprint tetap konsisten
projects_bp = Blueprint('projects_admin', __name__)

@projects_bp.route('/projects', methods=['GET'])
@login_required
def projects_page():
    return render_template('Frontend/admin/projects.html')


@projects_bp.route('/api/projects', methods=['GET', 'POST'])
@login_required
def handle_projects():
    # Ambil instance database dari app.py secara global
    db = current_app.get_db()
    
    if request.method == 'POST':
        data = request.get_json()
        judul = data.get('judul_proyek')
        deskripsi = data.get('deskripsi')
        link = data.get('link_proyek')
        gambar_url = data.get('gambar_url') # Hasil URL dari Cloudinary via frontend
        
        try:
            with db.cursor() as cursor:
                sql = """
                    INSERT INTO projects (judul_proyek, deskripsi, link_proyek, gambar_url) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (judul, deskripsi, link, gambar_url))
                db.commit() # Simpan permanen perubahan ke TiDB Cloud
            return jsonify({"success": True, "message": "Proyek berhasil ditambahkan ke database!"})
        except Exception as e:
            # Jika ada kegagalan koneksi atau query, batalkan transaksinya
            db.rollback()
            return jsonify({"success": False, "message": f"Gagal menyimpan ke database: {str(e)}"}), 500
        
    # Jika request bertipe GET (Menampilkan semua proyek untuk Admin Panel / Halaman Utama)
    try:
        with db.cursor() as cursor:
            # Mengambil seluruh baris proyek diurutkan dari yang terbaru (ID terbesar)
            cursor.execute("SELECT id, judul_proyek, deskripsi, link_proyek, gambar_url FROM projects ORDER BY id DESC")
            all_projects = cursor.fetchall()
        return jsonify(all_projects)
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil data: {str(e)}"}), 500


@projects_bp.route('/api/projects/<int:id>', methods=['PUT'])
@login_required
def update_project(id):
    db = current_app.get_db()
    data = request.get_json()
    judul = data.get('judul_proyek')
    deskripsi = data.get('deskripsi')
    link = data.get('link_proyek')
    gambar_url = data.get('gambar_url')
    
    if not judul:
        return jsonify({"success": False, "message": "Judul proyek wajib diisi"}), 400
        
    try:
        with db.cursor() as cursor:
            sql = """
                UPDATE projects 
                SET judul_proyek = %s, deskripsi = %s, link_proyek = %s, gambar_url = %s 
                WHERE id = %s
            """
            cursor.execute(sql, (judul, deskripsi, link, gambar_url, id))
            db.commit()
        return jsonify({"success": True, "message": "Proyek berhasil diperbarui!"})
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal memperbarui data: {str(e)}"}), 500


@projects_bp.route('/api/projects/<int:id>', methods=['DELETE'])
@login_required
def delete_project(id):
    db = current_app.get_db()
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM projects WHERE id = %s"
            cursor.execute(sql, (id,))
            db.commit()
        return jsonify({"success": True, "message": "Proyek berhasil dihapus!"})
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal menghapus data: {str(e)}"}), 500