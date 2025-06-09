from sqlalchemy.orm import Session
from src.models.models import Contact
from src.wrappers.dbSessionWrapper import with_db_session
from src.utils.logger import setup_logger
from typing import Optional


logger = setup_logger()

class ContactRepository:
    
    # Create a new resource
    @with_db_session
    def create_contact(self, contact: Contact, scoped_db: Session) -> Contact:
        try:
            logger.info(f"Creating contact: {contact.email}")
            
            db_contact = Contact(
                name=contact.name,
                phone_number=contact.phone_number,
                email=contact.email,
            )
            scoped_db.add(db_contact)
            scoped_db.commit()
            scoped_db.refresh(db_contact)
            logger.info(f"Contact created successfully: {db_contact.email}")
            return db_contact
        except Exception as e:
            logger.error(f"Error creating contact: {e}")
            raise Exception(f"Error in ContactRepository.create_contact: {e}")
    
    # List all resources
    @with_db_session
    def get_all_contacts(self, scoped_db: Session) -> list[Contact]:
        try:
            logger.info("Fetching all contacts")
            db_contacts = (
                scoped_db.query(Contact)
                .all()
            )
            return db_contacts
        except Exception as e:
            logger.error(f"Error getting all contacts: {e}")
            raise Exception(f"Error in ContactRepository.get_all_contacts: {e}")
        
    # Retrieve a specific resource
    @with_db_session
    def get_contact_by_number(self, phone_number: str, scoped_db: Session) -> Optional[Contact]:
        try:
            logger.info(f"Fetching contact with Number: {phone_number}")
            db_contact = scoped_db.query(Contact).filter(Contact.phone_number == phone_number).first()

            if not db_contact:
              return None
          
            logger.info(f"Contact with phone number: {phone_number} found.")
            return db_contact
        
        except Exception as e:
            logger.error(f"Error getting contact with phone number {phone_number}: {e}")
            raise Exception(f"Error in ContactRepository.get_contact_by_number: {e}")
    
    # Retrieve a specific resource
    @with_db_session
    def get_contact_by_email(self, email: str, scoped_db: Session) -> Optional[Contact]:
        try:
            logger.info(f"Fetching contact with email: {email}")
            db_contact = scoped_db.query(Contact).filter(Contact.email == email).first()

            if not db_contact:
              return None
          
            logger.info(f"Contact with email: {email} found.")
            return db_contact
        
        except Exception as e:
            logger.error(f"Error getting contact with phone email {email}: {e}")
            raise Exception(f"Error in ContactRepository.get_contact_by_email: {e}")