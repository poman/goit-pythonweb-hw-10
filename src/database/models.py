from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    Date,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from src.database.db import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    additional_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Contact(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')>"
