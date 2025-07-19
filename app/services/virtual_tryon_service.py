
from app.schemas.complete_look_response import CompleteLookResponse
from app.schemas.tryon_response import TryOnResponse
from dressing_in_order.models.dior_model import DIORModel
from app.schemas.clothing_item import ClothingItemSchema as ClothingItem

import torch
from PIL import Image
import torchvision.transforms as transforms
import os

class VirtualTryOnService:
    def __init__(self):
        # Initialize DiorModel (adjust based on dressing_in_order/models/dior_model.py)
        self.checkpoint_path = "D:/final_project/dressing_in_order/checkpoints/dior_model.pth"
        self.model = DIORModel()  # May require additional parameters
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if os.path.exists(self.checkpoint_path):
            self.model.load_state_dict(torch.load(self.checkpoint_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        # Define image transform
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])

    def process_image(self, image_path: str) -> torch.Tensor:
        """Helper method to process images."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        image = Image.open(image_path).convert("RGB")
        return self.transform(image).unsqueeze(0).to(self.device)

    async def generate_complete_look(self, clothing_items: list[ClothingItem]) -> CompleteLookResponse:
        try:
            # Placeholder: Implement logic to combine clothing items into a complete look
            clothing_tensors = [self.process_image(item.image_url) for item in clothing_items]
            with torch.no_grad():
                output = self.model(clothing_tensors)  # Adjust based on DiorModel
            output_image = "D:/final_project/output/complete_look.jpg"
            os.makedirs(os.path.dirname(output_image), exist_ok=True)
            transforms.ToPILImage()(output.squeeze(0).cpu()).save(output_image)
            return CompleteLookResponse(
                image_url=output_image,
                description="Generated complete look from provided clothing items"
            )
        except Exception as e:
            raise Exception(f"Error generating complete look: {str(e)}")

    async def virtual_tryon(self, clothing_item: ClothingItem, user_image: str) -> TryOnResponse:
        try:
            # Process user image and clothing item
            user_img_tensor = self.process_image(user_image)
            clothing_img_tensor = self.process_image(clothing_item.image_url)
            processed_pose = process_pose(user_image)  # Use pose_utils
            with torch.no_grad():
                output = self.model(user_img_tensor, clothing_img_tensor, processed_pose)
            output_image = "D:/final_project/output/tryon_image.jpg"
            os.makedirs(os.path.dirname(output_image), exist_ok=True)
            transforms.ToPILImage()(output.squeeze(0).cpu()).save(output_image)
            return TryOnResponse(
                tryon_image_url=output_image,
                message="Virtual try-on completed successfully"
            )
        except Exception as e:
            raise Exception(f"Error performing virtual try-on: {str(e)}")

# Instantiate service
virtual_tryon_service = VirtualTryOnService()

# Export functions for router
async def generate_complete_look(clothing_items: list[ClothingItem]) -> CompleteLookResponse:
    return await virtual_tryon_service.generate_complete_look(clothing_items)

async def virtual_tryon(clothing_item: ClothingItem, user_image: str) -> TryOnResponse:
    return await virtual_tryon_service.virtual_tryon(clothing_item, user_image)