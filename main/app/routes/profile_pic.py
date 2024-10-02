#Upload profile picture
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from fastapi import APIRouter,UploadFile, File, HTTPException,Depends
from ..database import database
from ..database.config import SECRET_KEY
from sqlalchemy.orm import Session
from ..dependencies.user_oauth2 import get_current_user
from ..database.config import api_secret
from ..models.profile_pic_model import Profile_Pictures
from ..schemas.profile_picture_schemas import ShowProfilePIc

import json

router = APIRouter(
    tags= ['profile_pic']
)

# Configuration       
cloudinary.config( 
    cloud_name = "drof2shjx", 
    api_key = "198289777728768", 
    api_secret = api_secret, # Click 'View API Keys' above to copy your API secret
    secure=True
)


@router.get('/get_profile_picture',response_model=ShowProfilePIc)
def get_profile_pic(db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    profile_pic = (
        db.query(Profile_Pictures).filter(Profile_Pictures.user_id == current_user).first()
    )
    return profile_pic


#upload profile picture
@router.post('/upload_profile_pic')
def upload_profile_pic(image:UploadFile, db:Session=Depends(database.get_db),
                      current_user=Depends(get_current_user)
                       ):
    profile_pic = (
        db.query(Profile_Pictures).filter(Profile_Pictures.user_id == current_user).first()
    )
    if profile_pic:
        raise HTTPException(status_code=400, detail="Can't upload picture twice go and edit profile picture")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid format. Only Image are allowed")
    
    # Upload the image to Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(image.file, public_id=f"attendenace_profile_pics/{current_user}")
        user_profile_pic = Profile_Pictures(user_id = current_user, picture_url = upload_result["secure_url"])
        
        db.add(user_profile_pic)
        db.commit()
        db.refresh(user_profile_pic)
        
        return {
            "message": "Profile picture uploaded successfully",
            "url": user_profile_pic.picture_url,
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
        updated_pic = db.query(Profile_Pictures).filter(Profile_Pictures.user_id == current_user)
        updated_image = upload_result["secure_url"]
        image_def = {'picture_url': updated_image}
        updated_pic.update(image_def)
        db.commit()
        # db.refresh(updated_pic)
        
        return {
            "message": "Profile picture updated successfully",
            "url": updated_pic.first().picture_url,
            # "public_id": upload_result["public_id"]
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