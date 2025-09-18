from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PetProfile(BaseModel):
    """Pet profile data model"""
    pet_id: str
    user_id: str
    name : str
    date_of_birth: datetime
    category: str
    gender: str
    breed: str
    age : int
    age_group: str
    health_conditions: List[str] = Field(default_factory=list)
    known_allergies: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        # Allow ObjectId to be used
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        
        
class PetProfileResponse(BaseModel):
    """Response model for pet profile"""
    pet_id: str
    name: str
    category: str
    age_group: str
    known_allergies: List[str]
    health_conditions: List[str]