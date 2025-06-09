from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.services.contactService import ContactService
from src.schemas.schemas import (
    Contact as ContactSchema
)
from src.utils.logger import setup_logger
from src.utils.dependencies import valid_auth_token

router = APIRouter(
    prefix="/contact", 
    tags=["contacts"],
    responses={404: {"description": "Not found"}},
    dependencies=[
         Depends(valid_auth_token)
    ]
)
logger = setup_logger() 
    
    
# Testing Endpoint
@router.get("/get-health")
async def get_health() -> JSONResponse:
    try:
        return JSONResponse(
            {"status": "good"}
        )
    except HTTPException as e:
        raise e

# Create a new resource
@router.post("/add", response_model=ContactSchema)
async def add_contact_endpoint(contact: ContactSchema) -> ContactSchema:
    logger.info(f"Received request to create contact: {contact.email}")
    contact_service = ContactService()
    try:
        db_contact = contact_service.add_new_contact(contact)
        logger.info(f"Contact created successfully: {db_contact.email}")
        return db_contact
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
# List all resources
@router.get("/get-all-contacts", response_model=list[ContactSchema])
async def get_all_contacts_endpoint(contact_service: ContactService = Depends()) -> list[ContactSchema]:
    try:
        return contact_service.get_all_contacts()
    except HTTPException as e:
        raise e

# Retrieve a specific resource
@router.get("/{phone_number}", response_model=ContactSchema)
async def get_contact_endpoint(phone_number: str) -> ContactSchema:
    contact_service = ContactService()
    try:
        db_contact = contact_service.get_contact(phone_number)
        return db_contact
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=400, detail=str(e))