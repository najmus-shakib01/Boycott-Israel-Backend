import os
import re
import uuid
import mimetypes
from django.conf import settings
from supabase import create_client, Client
import environ

env = environ.Env()

def get_supabase_client() -> Client:
    url = getattr(settings, 'SUPABASE_URL', env('SUPABASE_URL', default='https://hsacrlaaucymzmctggwp.supabase.co'))
    key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '') or getattr(settings, 'SUPABASE_ANON_KEY', '') or env('SUPABASE_ANON_KEY', default='')
    if not key:
        raise ValueError("SUPABASE_ANON_KEY বা SUPABASE_SERVICE_ROLE_KEY কনফিগার করা নেই।")
    return create_client(url, key)

def upload_to_supabase(file_obj, folder: str = "photos") -> str:
    """
    ফাইলকে সরাসরি সুপাবেস স্টোরেজের নির্দিষ্ট ফোল্ডারে আপলোড করে পাবলিক URL রিটার্ন করে।
    folder: 'photos' | 'videos' | 'products'
    """
    bucket_name = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'media')
    supabase = get_supabase_client()

    original_name = getattr(file_obj, 'name', 'file')
    ext = os.path.splitext(original_name)[1].lower()
    clean_base = re.sub(r'[^a-zA-Z0-9_\-]', '_', os.path.splitext(original_name)[0])
    unique_name = f"{uuid.uuid4().hex[:12]}_{clean_base}{ext}"
    storage_path = f"{folder}/{unique_name}"

    # Content Type
    content_type = getattr(file_obj, 'content_type', None)
    if not content_type:
        content_type = mimetypes.guess_type(original_name)[0] or 'application/octet-stream'

    # Read bytes
    if hasattr(file_obj, 'read'):
        file_obj.seek(0)
        data = file_obj.read()
    else:
        data = file_obj

    supabase.storage.from_(bucket_name).upload(
        storage_path,
        data,
        file_options={"content-type": content_type, "upsert": "true"}
    )

    return supabase.storage.from_(bucket_name).get_public_url(storage_path)
