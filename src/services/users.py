from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import User
from src.schemas import UserCreate
from src.services.auth import auth_service


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        if self.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        if self.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists"
            )

        hashed_password = auth_service.get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not auth_service.verify_password(password, user.hashed_password):
            return None
        return user

    def confirmed_email(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user:
            user.is_verified = True
            self.db.commit()

    def update_avatar(self, email: str, url: str) -> User:
        user = self.get_user_by_email(email)
        if user:
            user.avatar = url
            self.db.commit()
            self.db.refresh(user)
        return user