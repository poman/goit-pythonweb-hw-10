from typing import List, Optional
from sqlalchemy.orm import Session

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate, ContactResponse


class ContactService:
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)

    def create_contact(self, contact: ContactCreate, user_id: int) -> ContactResponse:
        db_contact = self.repository.create_contact(contact, user_id)
        return ContactResponse.model_validate(db_contact)

    def get_contact(self, contact_id: int, user_id: int) -> Optional[ContactResponse]:
        db_contact = self.repository.get_contact(contact_id, user_id)
        if db_contact:
            return ContactResponse.model_validate(db_contact)
        return None

    def get_contacts(self, skip: int = 0, limit: int = 100, user_id: int = None) -> List[ContactResponse]:
        db_contacts = self.repository.get_contacts(skip, limit, user_id)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]

    def update_contact(self, contact_id: int, contact: ContactUpdate, user_id: int) -> Optional[ContactResponse]:
        db_contact = self.repository.update_contact(contact_id, contact, user_id)
        if db_contact:
            return ContactResponse.model_validate(db_contact)
        return None

    def delete_contact(self, contact_id: int, user_id: int) -> bool:
        return self.repository.delete_contact(contact_id, user_id)

    def search_contacts(
            self,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            email: Optional[str] = None,
            user_id: int = None
    ) -> List[ContactResponse]:
        db_contacts = self.repository.search_contacts(first_name, last_name, email, user_id)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]

    def get_upcoming_birthdays(self, days: int = 7, user_id: int = None) -> List[ContactResponse]:
        db_contacts = self.repository.get_upcoming_birthdays(days, user_id)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]
