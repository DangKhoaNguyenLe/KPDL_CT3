from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class TourModel(BaseModel):
    id: int # Keep integer ID to be compatible with frontend for now
    name: str
    destination: str
    duration: str
    price: float
    image: str
    category: str
    rating: float
    reviews: int
    description: str
    highlights: List[str]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class BookingModel(BaseModel):
    tour_id: int
    date: str
    guests: int
    total_price: float
    status: str = "pending"

class RecommendationResponse(BaseModel):
    combo_id: int
    combo_name: str = ""
    antecedents: str
    consequents: str
    support: float
    confidence: float
    lift: float

class UserModel(BaseModel):
    username: str
    password: str

class ServiceModel(BaseModel):
    name: str
    type: str
    price: float
    description: str

class ReviewModel(BaseModel):
    tour_id: int
    user_id: str
    rating: int
    comment: str
