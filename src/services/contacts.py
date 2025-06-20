from typing import List, Optional
from sqlalchemy.orm import Session

from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate, ContactResponse


class ContactService:
    def __init__(self, db: Session):
        self.repository = ContactRepository(db)

    def create_contact(self, contact: ContactCreate) -> ContactResponse:
        db_contact = self.repository.create_contact(contact)
        return ContactResponse.model_validate(db_contact)

    def get_contact(self, contact_id: int) -> Optional[ContactResponse]:
        db_contact = self.repository.get_contact(contact_id)
        if db_contact:
            return ContactResponse.model_validate(db_contact)
        return None

    def get_contacts(self, skip: int = 0, limit: int = 100) -> List[ContactResponse]:
        db_contacts = self.repository.get_contacts(skip, limit)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]

    def update_contact(self, contact_id: int, contact: ContactUpdate) -> Optional[ContactResponse]:
        db_contact = self.repository.update_contact(contact_id, contact)
        if db_contact:
            return ContactResponse.model_validate(db_contact)
        return None

    def delete_contact(self, contact_id: int) -> bool:
        return self.repository.delete_contact(contact_id)

    def search_contacts(
            self,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            email: Optional[str] = None
    ) -> List[ContactResponse]:
        db_contacts = self.repository.search_contacts(first_name, last_name, email)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]

    def get_upcoming_birthdays(self, days: int = 7) -> List[ContactResponse]:
        db_contacts = self.repository.get_upcoming_birthdays(days)
        return [ContactResponse.model_validate(contact) for contact in db_contacts]
