from flask import Flask, render_template, g
from config import Config
import pymysql
from Backend.utama.utama import utama_bp
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.projects import projects_bp
from Backend.admin.skills import skills_bp
from Backend.admin.experience import experience_bp
from Backend.admin.upload import upload_bp

# 1. Inisialisasi Flask (Membaca index.html langsung dari root)
app = Flask(__name__, template_folder='.', static_folder='Frontend')
app.config.from_object(Config)
app.secret_key = app.config.get('SECRET_KEY', 'kunci-rahasia-bebas-apa-saja')

# ==========================================================================
# KONFIGURASI DATABASE TiDB GLOBAL
# ==========================================================================
def get_db():
    """Membuka koneksi database baru jika belum ada untuk request saat ini"""
    if 'db' not in g:
        host = app.config.get('TIDB_HOST', 'localhost')
        user = app.config.get('TIDB_USER', 'root')
        password = app.config.get('TIDB_PASSWORD', '')
        database = app.config.get('TIDB_NAME', 'portfolio')
        port = int(app.config.get('TIDB_PORT', 4000))

        ssl_config = None
        # TiDB Cloud wajib SSL, aktifkan jika host bukan localhost
        if host and host != 'localhost' and host != '127.0.0.1':
            import ssl as ssl_module
            ssl_config = {'ca': None, 'check_hostname': False}

        g.db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl=ssl_config,
            cursorclass=pymysql.cursors.DictCursor # Data dikembalikan dalam bentuk Dictionary/JSON-ready
        )
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Menutup koneksi database otomatis setiap kali request selesai"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Tempelkan fungsi get_db ke objek app agar bisa diimport dengan mudah oleh file Blueprint lain
app.get_db = get_db


# ==========================================================================
# REGISTRASI BLUEPRINT Halaman & Admin Panel
# ==========================================================================
app.register_blueprint(utama_bp)
app.register_blueprint(login_bp, url_prefix='/admin')
app.register_blueprint(dashboard_bp, url_prefix='/admin')
app.register_blueprint(profiles_bp, url_prefix='/admin')
app.register_blueprint(projects_bp, url_prefix='/admin')
app.register_blueprint(skills_bp, url_prefix='/admin')
app.register_blueprint(experience_bp, url_prefix='/admin')

# Registrasi API Utility Upload Gambar Cloudinary
app.register_blueprint(upload_bp, url_prefix='/admin')


if __name__ == '__main__':
    app.run(debug=True, port=5000)