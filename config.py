import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TIDB_HOST = os.getenv('TiDB_HOST') or os.getenv('TIDB_HOST')
    TIDB_USER = os.getenv('TiDB_USER') or os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TiDB_PASSWORD') or os.getenv('TIDB_PASSWORD')
    TIDB_NAME = os.getenv('TiDB_NAME') or os.getenv('TIDB_DB')
    TIDB_PORT = int(os.getenv('TiDB_PORT') or os.getenv('TIDB_PORT', 4000))
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    SECRET_KEY = 'kunci_rahasia_bebas'
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')