from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.services.contacts import ContactService
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.api.utils import validate_contact_exists, validate_search_params
from src.api.dependencies import get_current_active_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(db)


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
        contact: ContactCreate,
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    return service.create_contact(contact, current_user.id)


@router.get("/", response_model=List[ContactResponse])
def get_contacts(
        skip: int = Query(0, ge=0, description="Number of contacts to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Number of contacts to return"),
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    return service.get_contacts(skip=skip, limit=limit, user_id=current_user.id)


@router.get("/search", response_model=List[ContactResponse])
def search_contacts(
        first_name: Optional[str] = Query(None, description="Search by first name"),
        last_name: Optional[str] = Query(None, description="Search by last name"),
        email: Optional[str] = Query(None, description="Search by email"),
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    validate_search_params(first_name, last_name, email)
    return service.search_contacts(first_name=first_name, last_name=last_name, email=email, user_id=current_user.id)


@router.get("/birthdays", response_model=List[ContactResponse])
def get_upcoming_birthdays(
        days: int = Query(7, ge=1, le=365, description="Number of days to look ahead"),
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    return service.get_upcoming_birthdays(days=days, user_id=current_user.id)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
        contact_id: int,
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    contact = service.get_contact(contact_id, current_user.id)
    validate_contact_exists(contact, contact_id)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
        contact_id: int,
        contact: ContactUpdate,
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    updated_contact = service.update_contact(contact_id, contact, current_user.id)
    validate_contact_exists(updated_contact, contact_id)
    return updated_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
        contact_id: int,
        current_user: User = Depends(get_current_active_user),
        service: ContactService = Depends(get_contact_service)
):
    success = service.delete_contact(contact_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
