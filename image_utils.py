import uuid
from io import BytesIO
from PIL import Image, ImageOps
import cloudinary
import cloudinary.uploader
from starlette.concurrency import run_in_threadpool
from config import settings


def _get_cloudinary_config():
    """Initialize Cloudinary configuration"""
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret.get_secret_value()
    )


def _upload_to_cloudinary(file_bytes: bytes, public_id: str) -> dict:
    
    """Upload image to Cloudinary (synchronous)"""
    _get_cloudinary_config()

    result = cloudinary.uploader.upload(
        file_bytes,
        public_id=public_id,
        folder="profile_pics",
        overwrite=True,
        resource_type="image",
        transformation=[
            {'width': 300, 'height': 300, 'crop': 'fill', 'gravity': 'auto'}
        ]
    )
    return result


def _delete_from_cloudinary(public_id: str) -> None:
    """Delete image from Cloudinary (synchronous)"""
    _get_cloudinary_config()
    cloudinary.uploader.destroy(
        f"profile_pics/{public_id}",
        resource_type="image"
    )


def process_profile_image(content: bytes) -> tuple[bytes, str]:
    """Process image and return processed bytes + filename"""
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        # Save to BytesIO buffer
        output = BytesIO()
        img.save(output, "JPEG", quality=85, optimize=True)
        output.seek(0)

        filename = f"{uuid.uuid4().hex}.jpg"
        processed_bytes = output.getvalue()

        return processed_bytes, filename


async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    """Upload processed image to Cloudinary (async wrapper)"""
    # Remove .jpg extension for public_id
    public_id = filename.replace('.jpg', '')
    await run_in_threadpool(_upload_to_cloudinary, file_bytes, public_id)


async def delete_profile_image(filename: str | None) -> None:
    """Delete image from Cloudinary (async wrapper)"""
    if filename is None:
        return

    public_id = filename.replace('.jpg', '')
    try:
        await run_in_threadpool(_delete_from_cloudinary, public_id)
    except Exception:
        # Silently fail if image doesn't exist
        pass