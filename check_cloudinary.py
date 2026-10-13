from io import BytesIO
from PIL import Image
from cloudinary.exceptions import Error as CloudinaryError
from config import settings
from image_utils import _upload_to_cloudinary, _delete_from_cloudinary


def check_cloudinary_connection():
    print(f"Cloud Name: {settings.cloudinary_cloud_name}")
    print()

    test_public_id = "test_connection"

    # Create a simple test image (1x1 red pixel)
    img = Image.new('RGB', (1, 1), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    test_bytes = img_bytes.getvalue()

    try:
        _upload_to_cloudinary(test_bytes, test_public_id)
        print("Upload: SUCCESS")
    except CloudinaryError as exc:
        print(f"Upload: FAILED - {exc}")
        return

    try:
        _delete_from_cloudinary(test_public_id)
        print("Delete: SUCCESS")
    except CloudinaryError as exc:
        print(f"Delete: FAILED - {exc}")
        return

    print()
    print("All tests passed! Your Cloudinary configuration is working.")


if __name__ == "__main__":
    check_cloudinary_connection()