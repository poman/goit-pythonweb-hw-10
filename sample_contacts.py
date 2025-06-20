from datetime import date
from sqlalchemy.orm import Session

from src.database.db import SessionLocal, engine
from src.database.models import Base, Contact

Base.metadata.create_all(bind=engine)


def create_sample_contacts():
    db: Session = SessionLocal()

    try:
        if db.query(Contact).first():
            print("Database already has contacts. Skipping seed.")
            return

        sample_contacts = [
            Contact(
                first_name="Іван",
                last_name="Петренко",
                email="ivan.petrenko@example.com",
                phone_number="+380501234567",
                birthday=date(1990, 5, 15),
                additional_data="Software Engineer from Kyiv"
            ),
            Contact(
                first_name="Марія",
                last_name="Коваленко",
                email="maria.kovalenko@example.com",
                phone_number="+380671234567",
                birthday=date(1985, 8, 23),
                additional_data="Designer from Lviv"
            ),
            Contact(
                first_name="Олександр",
                last_name="Шевченко",
                email="alex.shevchenko@example.com",
                phone_number="+380931234567",
                birthday=date(1992, 12, 1),
                additional_data="Product Manager from Odesa"
            ),
            Contact(
                first_name="Анна",
                last_name="Мельник",
                email="anna.melnyk@example.com",
                phone_number="+380681234567",
                birthday=date(1988, 3, 18),
                additional_data="Data Scientist from Kharkiv"
            ),
            Contact(
                first_name="Дмитро",
                last_name="Бондаренко",
                email="dmytro.bondarenko@example.com",
                phone_number="+380501234568",
                birthday=date(1995, 7, 4),
                additional_data="DevOps Engineer from Dnipro"
            ),
            Contact(
                first_name="Олена",
                last_name="Гриценко",
                email="olena.grytsenko@example.com",
                phone_number="+380671234568",
                birthday=date(1987, 11, 30),
                additional_data="Business Analyst from Zaporizhzhia"
            ),
            Contact(
                first_name="Віктор",
                last_name="Савченко",
                email="viktor.savchenko@example.com",
                phone_number="+380931234568",
                birthday=date(1991, 1, 14),
                additional_data="QA Engineer from Poltava"
            ),
            Contact(
                first_name="Тетяна",
                last_name="Лисенко",
                email="tetiana.lysenko@example.com",
                phone_number="+380681234568",
                birthday=date(1993, 9, 8),
                additional_data="Frontend Developer from Chernivtsi"
            ),
        ]

        db.add_all(sample_contacts)
        db.commit()

        print(f"Successfully created {len(sample_contacts)} sample contacts!")

    except Exception as e:
        print(f"Error creating sample contacts: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_contacts()
