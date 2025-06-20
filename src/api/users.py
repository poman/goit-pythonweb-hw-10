from fastapi import APIRouter, Depends, UploadFile, File, Request
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserResponse
from src.services.users import UserService
from src.services.cloudinary import CloudinaryService
from src.api.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/me/", response_model=UserResponse)
@limiter.limit("10/minute")
def read_users_me(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.patch("/avatar", response_model=UserResponse)
def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(get_current_active_user),
    service: UserService = Depends(get_user_service)
):
    try:
        cloudinary_service = CloudinaryService()
        r = cloudinary_service.upload_file(file, current_user.username) 
        src_url = cloudinary_service.get_url_for_avatar(r['public_id'], r)
        user = service.update_avatar(current_user.email, src_url)
        return user
    except Exception as e:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload avatar: {str(e)}"
        )