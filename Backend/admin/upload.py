# Backend/admin/upload.py
from flask import Blueprint, request, jsonify, session
import cloudinary
import cloudinary.uploader
from config import Config
from Backend.admin.login import login_required

upload_bp = Blueprint('upload_admin', __name__)

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

@upload_bp.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Tidak ada berkas gambar"}), 400
        
    file_to_upload = request.files['file']
    if file_to_upload:
        try:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            return jsonify({
                "success": True, 
                "secure_url": upload_result.get("secure_url")
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500