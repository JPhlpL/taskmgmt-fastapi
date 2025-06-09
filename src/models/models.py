from sqlalchemy import String, DateTime
from datetime import datetime, timezone
from uuid import UUID as PyUUID, uuid4
from sqlalchemy.dialects.postgresql import UUID
import uuid
# from src.database.config import get_database_engine  # Import the function to get the engine
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    DeclarativeBase
)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

# engine = get_database_engine()  # Call the function to get the engine
# Base.metadata.create_all(bind=engine)
