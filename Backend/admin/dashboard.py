from flask import Blueprint, render_template, jsonify, current_app
from Backend.admin.login import login_required

# Sesuaikan nama variabel dengan registrasi di app.py (dashboard_bp)
# KOREKSI: Gunakan 'dashboard_admin' agar sinkron dengan file app.py Anda
dashboard_bp = Blueprint('dashboard_admin', __name__)

# 1. Menampilkan Tampilan Utama Dashboard Admin
# KOREKSI: Cukup '/dashboard' karena '/admin' sudah dicakup url_prefix di app.py
@dashboard_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('Frontend/admin/dashboard.html')


# 2. API Hitung Statistik Real-Time dari TiDB Cloud
@dashboard_bp.route('/api/admin/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    db = current_app.get_db()
    try:
        with db.cursor() as cursor:
            # 1. Hitung total proyek yang tersimpan
            cursor.execute("SELECT COUNT(*) as total FROM projects")
            total_projects = cursor.fetchone()['total']
            
            # 2. Hitung total keahlian / skills
            cursor.execute("SELECT COUNT(*) as total FROM skills")
            total_skills = cursor.fetchone()['total']
            
            # 3. Hitung total riwayat pengalaman
            cursor.execute("SELECT COUNT(*) as total FROM pengalaman")
            total_experience = cursor.fetchone()['total']
            
            # 4. Hitung total pesan masuk dari formulir kontak di portofolio depan
            cursor.execute("SELECT COUNT(*) as total FROM kontak")
            total_messages = cursor.fetchone()['total']
            
        return jsonify({
            "success": True,
            "stats": {
                "projects": total_projects,
                "skills": total_skills,
                "experience": total_experience,
                "messages": total_messages
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Gagal menghitung statistik: {str(e)}"}), 500