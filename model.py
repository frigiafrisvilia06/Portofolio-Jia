import pymysql
from config import Config

def get_db_connection():
    host = Config.TIDB_HOST or 'localhost'
    ssl_config = None
    if host and host != 'localhost' and host != '127.0.0.1':
        ssl_config = {'ca': None, 'check_hostname': False}

    connection = pymysql.connect(
        host=host,
        user=Config.TIDB_USER,
        password=Config.TIDB_PASSWORD,
        database=Config.TIDB_NAME,
        port=Config.TIDB_PORT,
        ssl=ssl_config,
        cursorclass=pymysql.cursors.DictCursor  
    )
    return connection

# =========================================
# PROFIL CRUD
# =========================================
def get_profil():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM profil ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()
    finally:
        connection.close()

def update_profil(profile_id, nama, peran, deskripsi, foto_url):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if profile_id:
                sql = "UPDATE profil SET nama=%s, peran=%s, deskripsi=%s, foto_url=%s WHERE id=%s"
                cursor.execute(sql, (nama, peran, deskripsi, foto_url, profile_id))
            else:
                sql = "INSERT INTO profil (nama, peran, deskripsi, foto_url) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nama, peran, deskripsi, foto_url))
        connection.commit()
        return True
    finally:
        connection.close()

# =========================================
# SKILLS CRUD
# =========================================
def get_all_skills():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM skills ORDER BY id ASC")
            return cursor.fetchall()
    finally:
        connection.close()

def insert_skill(nama_skill, kategori):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO skills (nama_skill, kategori) VALUES (%s, %s)"
            cursor.execute(sql, (nama_skill, kategori))
        connection.commit()
        return True
    finally:
        connection.close()

def update_skill(id_skill, nama_skill, kategori):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE skills SET nama_skill=%s, kategori=%s WHERE id=%s"
            cursor.execute(sql, (nama_skill, kategori, id_skill))
        connection.commit()
        return True
    finally:
        connection.close()

def delete_skill(id_skill):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM skills WHERE id=%s"
            cursor.execute(sql, (id_skill,))
        connection.commit()
        return True
    finally:
        connection.close()

# =========================================
# PROJECTS CRUD
# =========================================
def get_all_projects():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            return cursor.fetchall()
    finally:
        connection.close()

def insert_project(judul_proyek, deskripsi, link_proyek, gambar_url):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO projects (judul_proyek, deskripsi, link_proyek, gambar_url) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (judul_proyek, deskripsi, link_proyek, gambar_url))
        connection.commit()
        return True
    finally:
        connection.close()

def update_project(id_proyek, judul_proyek, deskripsi, link_proyek, gambar_url):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE projects SET judul_proyek=%s, deskripsi=%s, link_proyek=%s, gambar_url=%s WHERE id=%s"
            cursor.execute(sql, (judul_proyek, deskripsi, link_proyek, gambar_url, id_proyek))
        connection.commit()
        return True
    finally:
        connection.close()

def delete_project(id_proyek):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM projects WHERE id=%s"
            cursor.execute(sql, (id_proyek,))
        connection.commit()
        return True
    finally:
        connection.close()

# =========================================
# PENGALAMAN CRUD
# =========================================
def get_all_pengalaman():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pengalaman ORDER BY id DESC")
            return cursor.fetchall()
    finally:
        connection.close()

def insert_pengalaman(perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO pengalaman (perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi))
        connection.commit()
        return True
    finally:
        connection.close()

def update_pengalaman(id_exp, perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            UPDATE pengalaman 
            SET perusahaan_organisasi=%s, posisi=%s, tanggal_mulai=%s, tanggal_selesai=%s, deskripsi=%s 
            WHERE id=%s
            """
            cursor.execute(sql, (perusahaan_organisasi, posisi, tanggal_mulai, tanggal_selesai, deskripsi, id_exp))
        connection.commit()
        return True
    finally:
        connection.close()

def delete_pengalaman(id_exp):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM pengalaman WHERE id=%s"
            cursor.execute(sql, (id_exp,))
        connection.commit()
        return True
    finally:
        connection.close()