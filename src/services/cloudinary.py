import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class CloudinaryService:
    def __init__(self):
        print(f"Cloudinary config - Name: {settings.cloudinary_name}, API Key: {settings.cloudinary_api_key}")
        
        cloudinary.config(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )

    @staticmethod
    def upload_file(file, username: str):
        public_id = f"ContactsApp/{username}"
        file_content = file.file.read()
        r = cloudinary.uploader.upload(file_content, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_avatar(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id)\
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url