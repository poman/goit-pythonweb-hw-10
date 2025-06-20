from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_contact(self, contact_id: int, user_id: int) -> Optional[Contact]:
        return self.db.query(Contact).filter(
            Contact.id == contact_id, Contact.user_id == user_id
        ).first()

    def get_contacts(self, skip: int = 0, limit: int = 100, user_id: int = None) -> List[Contact]:
        query = self.db.query(Contact)
        if user_id:
            query = query.filter(Contact.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    def create_contact(self, contact: ContactCreate, user_id: int) -> Contact:
        contact_data = contact.model_dump()
        contact_data["user_id"] = user_id
        db_contact = Contact(**contact_data)
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact

    def update_contact(self, contact_id: int, contact: ContactUpdate, user_id: int) -> Optional[Contact]:
        db_contact = self.get_contact(contact_id, user_id)
        if db_contact:
            contact_data = contact.model_dump(exclude_unset=True)
            for field, value in contact_data.items():
                setattr(db_contact, field, value)
            self.db.commit()
            self.db.refresh(db_contact)
        return db_contact

    def delete_contact(self, contact_id: int, user_id: int) -> bool:
        db_contact = self.get_contact(contact_id, user_id)
        if db_contact:
            self.db.delete(db_contact)
            self.db.commit()
            return True
        return False

    def search_contacts(
            self,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            email: Optional[str] = None,
            user_id: int = None
    ) -> List[Contact]:
        query = self.db.query(Contact)
        
        if user_id:
            query = query.filter(Contact.user_id == user_id)

        conditions = []
        if first_name:
            conditions.append(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            conditions.append(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            conditions.append(Contact.email.ilike(f"%{email}%"))

        if conditions:
            query = query.filter(or_(*conditions))

        return query.all()

    def get_upcoming_birthdays(self, days: int = 7, user_id: int = None) -> List[Contact]:
        today = date.today()
        end_date = today + timedelta(days=days)

        query = self.db.query(Contact)
        
        if user_id:
            query = query.filter(Contact.user_id == user_id)

        if today.year == end_date.year:
            return query.filter(
                and_(
                    extract('month', Contact.birthday) >= today.month,
                    extract('month', Contact.birthday) <= end_date.month,
                    or_(
                        extract('month', Contact.birthday) > today.month,
                        and_(
                            extract('month', Contact.birthday) == today.month,
                            extract('day', Contact.birthday) >= today.day
                        )
                    ),
                    or_(
                        extract('month', Contact.birthday) < end_date.month,
                        and_(
                            extract('month', Contact.birthday) == end_date.month,
                            extract('day', Contact.birthday) <= end_date.day
                        )
                    )
                )
            ).all()
        else:
            return query.filter(
                or_(
                    and_(
                        extract('month', Contact.birthday) >= today.month,
                        or_(
                            extract('month', Contact.birthday) > today.month,
                            and_(
                                extract('month', Contact.birthday) == today.month,
                                extract('day', Contact.birthday) >= today.day
                            )
                        )
                    ),
                    and_(
                        extract('month', Contact.birthday) <= end_date.month,
                        or_(
                            extract('month', Contact.birthday) < end_date.month,
                            and_(
                                extract('month', Contact.birthday) == end_date.month,
                                extract('day', Contact.birthday) <= end_date.day
                            )
                        )
                    )
                )
            ).all()
