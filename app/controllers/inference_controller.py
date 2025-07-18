import requests
import cloudinary.uploader
from models.schemas import VirtualTryOnRequest, TryOnResponse
import uuid
import os

class InferenceController:
    def download_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            raise Exception(f"Failed to download image: {url}")

    def generate_try_on_image(self, request: VirtualTryOnRequest) -> TryOnResponse:
        user_img = f"temp_user_{uuid.uuid4().hex}.jpg"
        cloth_img = f"temp_cloth_{uuid.uuid4().hex}.jpg"

        self.download_image(request.user_image_url, user_img)
        self.download_image(request.clothing_image_url, cloth_img)

        # Replace this line with your actual model inference
        output_img = f"output_{uuid.uuid4().hex}.jpg"
        os.system(f"copy {user_img} {output_img}")  # Dummy placeholder

        upload_result = cloudinary.uploader.upload(output_img)
        output_url = upload_result.get("secure_url")

        for f in [user_img, cloth_img, output_img]:
            if os.path.exists(f):
                os.remove(f)

        return TryOnResponse(tryon_image_url=output_url)
