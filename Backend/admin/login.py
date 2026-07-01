from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from functools import wraps

# Sesuaikan nama blueprint dengan registrasi di app.py Anda (login_bp)
login_bp = Blueprint('login_bp', __name__)

# --- TAMBAHAN BARU: Fungsi Pengunci Halaman (Decorator) ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Silakan login terlebih dahulu!')
            return redirect(url_for('login_bp.admin_login'))
        return f(*args, **kwargs)
    return decorated_function
# ----------------------------------------------------------


@login_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Menggunakan koneksi database global dari app.py
        db = current_app.get_db()
        try:
            with db.cursor() as cursor:
                # Mencari user di tabel admin TiDB Cloud
                sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                
                if user:
                    session['logged_in'] = True
                    # Karena get_db() menggunakan DictCursor, user pasti berupa dictionary
                    session['username'] = user['username']
                    
                    # PERBAIKAN UTAMA: Diarahkan ke nama blueprint dashboard yang baru (dashboard_admin)
                    return redirect(url_for('dashboard_admin.admin_dashboard'))
                else:
                    flash('Username atau Password salah!')
        except Exception as e:
            flash(f'Terjadi kesalahan database: {str(e)}')

    return render_template('Frontend/admin/login.html')


@login_bp.route('/logout')
def admin_logout():
    session.clear()
    # Jika request dari AJAX (fetch API di base.js), kembalikan JSON
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        return jsonify({"success": True, "redirect": "/admin/login"})
    # Jika request dari navigasi biasa (<a> tag), redirect langsung
    return redirect(url_for('utama.index'))


# --- API UBAH PASSWORD ---
@login_bp.route('/api/change-password', methods=['PUT'])
@login_required
def change_password():
    db = current_app.get_db()
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({"success": False, "message": "Password lama dan password baru wajib diisi"}), 400

    username = session.get('username')
    try:
        with db.cursor() as cursor:
            # Verifikasi password lama
            sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, current_password))
            user = cursor.fetchone()

            if not user:
                return jsonify({"success": False, "message": "Password saat ini salah"}), 401

            # Update password baru
            sql_update = "UPDATE admin SET password = %s WHERE username = %s"
            cursor.execute(sql_update, (new_password, username))
            db.commit()

        return jsonify({"success": True, "message": "Password berhasil diubah"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal mengubah password: {str(e)}"}), 500