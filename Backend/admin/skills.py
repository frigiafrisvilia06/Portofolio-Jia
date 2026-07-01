from flask import Blueprint, request, jsonify, render_template, current_app
from Backend.admin.login import login_required

skills_bp = Blueprint('skills_admin', __name__)

# 1. Menampilkan Halaman Skills
@skills_bp.route('/skills', methods=['GET'])
@login_required
def skills_page():
    return render_template('Frontend/admin/skills.html')


# 2. API Handle GET (Read) & POST (Create)
@skills_bp.route('/api/skills', methods=['GET', 'POST'])
@login_required
def handle_skills():
    db = current_app.get_db()
    
    if request.method == 'POST':
        data = request.get_json()
        nama_skill = data.get('nama_skill')
        kategori = data.get('kategori')
        
        if not nama_skill or not kategori:
            return jsonify({"success": False, "message": "Data tidak lengkap"}), 400
            
        try:
            with db.cursor() as cursor:
                sql = "INSERT INTO skills (nama_skill, kategori) VALUES (%s, %s)"
                cursor.execute(sql, (nama_skill, kategori))
                db.commit()
            return jsonify({"success": True, "message": "Skill berhasil ditambahkan ke TiDB!"}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"success": False, "message": f"Gagal menyimpan data: {str(e)}"}), 500
        
    # GET Request: Ambil semua skills
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id, nama_skill, kategori FROM skills ORDER BY id DESC")
            all_skills = cursor.fetchall()
        return jsonify(all_skills)
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal mengambil data: {str(e)}"}), 500


# 3. API Handle PUT (Update) - FITUR EDIT
@skills_bp.route('/api/skills/<int:id_skill>', methods=['PUT'])
@login_required
def update_skill(id_skill):
    db = current_app.get_db()
    data = request.get_json()
    nama_skill = data.get('nama_skill')
    kategori = data.get('kategori')
    
    if not nama_skill or not kategori:
        return jsonify({"success": False, "message": "Data tidak lengkap"}), 400
        
    try:
        with db.cursor() as cursor:
            sql = "UPDATE skills SET nama_skill = %s, kategori = %s WHERE id = %s"
            cursor.execute(sql, (nama_skill, kategori, id_skill))
            db.commit()
        return jsonify({"success": True, "message": "Skill berhasil diperbarui di TiDB!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal memperbarui data: {str(e)}"}), 500


# 4. API Handle DELETE (Hapus)
@skills_bp.route('/api/skills/<int:id_skill>', methods=['DELETE'])
@login_required
def remove_skill(id_skill):
    db = current_app.get_db()
    
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM skills WHERE id = %s"
            cursor.execute(sql, (id_skill,))
            db.commit()
        return jsonify({"success": True, "message": "Skill berhasil dihapus dari TiDB!"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal menghapus data: {str(e)}"}), 500