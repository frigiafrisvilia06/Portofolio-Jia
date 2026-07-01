import resend
from flask import Blueprint, request, jsonify, render_template, current_app
from config import Config

utama_bp = Blueprint('utama', __name__)
resend.api_key = Config.RESEND_API_KEY

@utama_bp.route('/')
def index():
    # Mengambil instance database global dari app.py
    db = current_app.get_db()
    
    try:
        with db.cursor() as cursor:
            # 1. Ambil Data Diri / Profil (Baris pertama)
            cursor.execute("SELECT * FROM profil LIMIT 1")
            data_profil = cursor.fetchone() or {}
            
            # 2. Ambil Semua Keahlian / Skills (Diurutkan berdasarkan kategori)
            cursor.execute("SELECT * FROM skills ORDER BY kategori ASC")
            data_skills = cursor.fetchall()
            
            # 3. Ambil Riwayat Pengalaman (Diurutkan dari yang terbaru)
            cursor.execute("SELECT * FROM pengalaman ORDER BY id DESC")
            data_experience = cursor.fetchall()
            
            # 4. Ambil Semua Proyek (Diurutkan dari yang terbaru)
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            data_projects = cursor.fetchall()
            
        # Kirim semua data dari TiDB ke file HTML portofolio depan Anda (index.html)
        return render_template(
            'index.html', # Pastikan path ke file index.html portofolio depan Anda benar
            profil=data_profil,
            skills=data_skills,
            experiences=data_experience,
            projects=data_projects
        )
    except Exception as e:
        # Jika database bermasalah saat diakses pengunjung, beri fallback pesan error aman
        return f"Gagal memuat halaman portofolio: {str(e)}", 500


@utama_bp.route('/api/contact', methods=['POST'])
def contact():
    db = current_app.get_db()
    
    # Mendukung input JSON maupun Form Data standard
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
    
    if not name or not email or not message:
        return jsonify({"success": False, "message": "Semua field (Nama, Email, Pesan) wajib diisi!"}), 400
        
    subject = subject or "KerjaSama"
    
    # 1. Simpan pesan ke database TiDB menggunakan pool koneksi global
    db_message = f"Subjek: {subject}\n\n{message}"
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO kontak (nama_pengirim, email_pengirim, pesan) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, db_message))
            db.commit() # Lakukan commit transaksi ke TiDB Cloud
    except Exception as e:
        db.rollback()
        return jsonify({"success": False, "message": f"Gagal menyimpan ke database: {str(e)}"}), 500

    # 2. Kirim notifikasi email via Resend (Logika dipertahankan tetap sama)
    try:
        admin_email = Config.ADMIN_EMAIL or "frigia.frisvilia06@gmail.com"
        params = {
            "from": "Portfolio Contact <onboarding@resend.dev>",
            "to": [admin_email],
            "subject": f"Portfolio Contact: {subject}",
            "html": f"""
            <div style="font-family: sans-serif; line-height: 1.6; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
                <h2 style="font-size: 18px; margin-top: 0; margin-bottom: 16px; color: #111111; font-weight: 600;">New Contact Form Submission</h2>
                <p style="margin: 6px 0; font-size: 15px;"><strong>Name:</strong> {name}</p>
                <p style="margin: 6px 0; font-size: 15px;"><strong>Email:</strong> <a href="mailto:{email}" style="color: #2563eb; text-decoration: none;">{email}</a></p>
                <p style="margin: 6px 0; font-size: 15px;"><strong>Subject:</strong> {subject}</p>
                <p style="margin: 16px 0 6px 0; font-size: 15px;"><strong>Message:</strong></p>
                <div style="padding: 14px 18px; background-color: #f9fafb; border-left: 4px solid #8b5cf6; border-radius: 4px; white-space: pre-wrap; color: #1f2937; margin-top: 6px; font-size: 15px; border-top: 1px solid #f3f4f6; border-right: 1px solid #f3f4f6; border-bottom: 1px solid #f3f4f6;">{message}</div>
            </div>
            """
        }
        resend.Emails.send(params)
    except Exception as e:
        return jsonify({
            "success": True, 
            "message": f"Pesan berhasil disimpan di database, namun notifikasi email gagal dikirim: {str(e)}"
        }), 200

    return jsonify({"success": True, "message": "Pesan Anda berhasil dikirim dan disimpan!"}), 200