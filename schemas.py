"""
Database Schemas for Pacific Christian School

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date as DateType, datetime as DateTimeType

class Announcement(BaseModel):
    title: str = Field(..., description="Headline for the announcement")
    body: str = Field(..., description="Detailed announcement content")
    published_at: Optional[DateTimeType] = Field(None, description="Publish timestamp; defaults to now on the server")
    author: Optional[str] = Field(None, description="Name of the staff member who authored the announcement")

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    event_date: DateType = Field(..., description="Event date")
    location: Optional[str] = Field(None, description="Event location")

class Contactmessage(BaseModel):
    name: str = Field(..., description="Sender full name")
    email: EmailStr = Field(..., description="Sender email address")
    subject: str = Field(..., description="Message subject")
    message: str = Field(..., description="Message body")
