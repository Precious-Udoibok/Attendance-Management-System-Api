#Upload profile picture
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import APIRouter,UploadFile, File, HTTPException,Depends
from ..database import database
from ..database.config import SECRET_KEY
from sqlalchemy.orm import Session
from ..dependencies.user_oauth2 import get_current_user

router = APIRouter(
    tags= ['profile_pic']
)

# Configuration       
cloudinary.config( 
    cloud_name = "drof2shjx", 
    api_key = "198289777728768", 
    api_secret = "sNwpKVT1tsQ-uas4pkk14kYqPGw", # Click 'View API Keys' above to copy your API secret
    secure=True
)


#upload profile picture
@router.post('/upload_profile_pic')
def upload_profile_pic(image:UploadFile, db:Session=Depends(database.get_db),
                      current_user=Depends(get_current_user)
                       ):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid format. Only Image are allowed")
    
    # Upload the image to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(image.file, public_id=f"attendenace_profile_pics/{current_user}")
        return {
            "message": "Profile picture uploaded successfully",
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")
    
    
#Update the image
# Route to update profile picture
@router.put("/update_profile_pic")
def update_profile_pic(image:UploadFile, db:Session=Depends(database.get_db),
                      current_user=Depends(get_current_user)
                      ):
                          
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid format. Only Image are allowed")
    
    try:
        # Delete the old picture if it exists
        cloudinary.uploader.destroy(f"attendenace_profile_pics/{current_user}")

        # Upload the new profile picture
        upload_result = cloudinary.uploader.upload(image.file, public_id=f"attendenace_profile_pics/{current_user}")
        return {
            "message": "Profile picture updated successfully",
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary update failed: {str(e)}")


# # Upload an image
# upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#                                            public_id="shoes")
# print(upload_result["secure_url"])

# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
# print(optimize_url)

# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)