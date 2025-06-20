from typing import List, Optional
from fastapi import HTTPException, status


def validate_contact_exists(contact, contact_id: int):
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with id {contact_id} not found"
        )
    return contact


def validate_search_params(first_name: Optional[str], last_name: Optional[str], email: Optional[str]):
    if not any([first_name, last_name, email]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search parameter (first_name, last_name, or email) must be provided"
        )
