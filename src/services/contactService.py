from src.repositories.contactRepository import ContactRepository
from src.schemas.schemas import (
    Contact as ContactSchema
)
from src.models.models import Contact
from src.utils.logger import setup_logger
from fastapi import HTTPException  # Import HTTPException


logger = setup_logger()

class ContactService:
    def __init__(
        self
    ) -> None:
        self.contact_repository = ContactRepository()
        
    # ====================== Database Call ==================================

    # Create a new resource
    def add_new_contact(self, contact: ContactSchema) -> ContactSchema:
        # Check if the email already exists in the database
        existing_contact = self.contact_repository.get_contact_by_email(contact.email)
        if existing_contact:
            raise HTTPException(status_code=400, detail="Email already registered.")
        # Proceed to create the new contact
        try:
            logger.info(f"Creating new contact: {contact.email}")
            db_contact = self.contact_repository.create_contact(contact)
            return db_contact
        except Exception as e:
            logger.error(f"Error in adding a contact: {e}")
            raise Exception(f"Error in ContactService.add_new_contact: {e}")
    
    # List all resources
    def get_all_contacts(self) -> list[ContactSchema]:
        try:
            logger.info(f"Getting All Contacts")
            db_contact = self.contact_repository.get_all_contacts()
            if not db_contact:
                logger.warning(f"No contacts found")
                raise HTTPException(status_code=404, detail="Contacts not found")
            return db_contact
        except HTTPException as e:
            raise e
        
    # Retrieve a specific resource
    def get_contact(self, phone_number: str) -> ContactSchema:
        try:
            logger.info(f"Getting the contact detail of phone number: {phone_number}")
            db_contact = self.contact_repository.get_contact_by_number(phone_number)
            return db_contact
        except Exception as e:
            logger.error(f"Error in getting a contact: {e}")
            raise Exception(f"Error in ContactService.get_contact: {e}")

    
    # ====================== Schema Transform ==================================

    def transform_contact_model_to_schema(
        self, contact: Contact
    ) -> ContactSchema:
        return ContactSchema(**contact.__dict__)

    # ====================== Schema Transform ==================================