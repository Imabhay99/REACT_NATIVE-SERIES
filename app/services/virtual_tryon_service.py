from app.schemas.complete_look_response import CompleteLookResponse
from app.schemas.tryon_response import TryOnResponse
from dressing_in_order.models.dior_model import DIORModel
from app.schemas.clothing_item import ClothingItemSchema as ClothingItem

import torch
from PIL import Image
import torchvision.transforms as transforms
import os

# If you have a pose processing function, import it properly
# Example:
# from dressing_in_order.utils.pose_utils import process_pose

class VirtualTryOnService:
    def __init__(self):
        self.checkpoint_path = "D:/final_project/dressing_in_order/checkpoints/dior_model.pth"
        self.model = DIORModel()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if os.path.exists(self.checkpoint_path):
            self.model.load_state_dict(torch.load(self.checkpoint_path, map_location=self.device))
        else:
            raise FileNotFoundError(f"Checkpoint not found at {self.checkpoint_path}")

        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])

    def process_image(self, image_path: str) -> torch.Tensor:
        """Load and transform image into tensor."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        image = Image.open(image_path).convert("RGB")
        return self.transform(image).unsqueeze(0).to(self.device)

    async def generate_complete_look(self, clothing_items: list[ClothingItem]) -> CompleteLookResponse:
        try:
            # Load and process all clothing item images
            clothing_tensors = [self.process_image(item.image_url) for item in clothing_items]

            # Forward through model
            with torch.no_grad():
                output = self.model(clothing_tensors)  # Adjust this if model expects differently

            output_image_path = "D:/final_project/output/complete_look.jpg"
            os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
            transforms.ToPILImage()(output.squeeze(0).cpu()).save(output_image_path)

            return CompleteLookResponse(
                image_url=output_image_path,
                description="Generated complete look from provided clothing items"
            )
        except Exception as e:
            raise Exception(f"[Generate Complete Look Error] {str(e)}")

    async def virtual_tryon(self, clothing_item: ClothingItem, user_image_path: str) -> TryOnResponse:
        try:
            user_tensor = self.process_image(user_image_path)
            clothing_tensor = self.process_image(clothing_item.image_url)

            # Placeholder for pose processing
            # Replace with actual call to pose estimation if needed
            processed_pose = None
            # processed_pose = process_pose(user_image_path)

            # Forward through model
            with torch.no_grad():
                output = self.model(user_tensor, clothing_tensor, processed_pose)

            output_image_path = "D:/final_project/output/tryon_image.jpg"
            os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
            transforms.ToPILImage()(output.squeeze(0).cpu()).save(output_image_path)

            return TryOnResponse(
                tryon_image_url=output_image_path,
                message="Virtual try-on completed successfully"
            )
        except Exception as e:
            raise Exception(f"[Virtual Try-On Error] {str(e)}")

# Instantiate service
virtual_tryon_service = VirtualTryOnService()

# Exportable async wrappers
async def generate_complete_look(clothing_items: list[ClothingItem]) -> CompleteLookResponse:
    return await virtual_tryon_service.generate_complete_look(clothing_items)

async def virtual_tryon(clothing_item: ClothingItem, user_image: str) -> TryOnResponse:
    return await virtual_tryon_service.virtual_tryon(clothing_item, user_image)
