from fastapi import APIRouter, HTTPException, Body
from typing import List
from Backend.models import TourModel
from Backend.database import tours_collection

router = APIRouter(
    prefix="/tours",
    tags=["Tours"]
)

@router.get("/", response_model=List[TourModel])
async def get_tours():
    tours = []
    async for tour in tours_collection.find():
        tours.append(TourModel(**tour))
    return tours

@router.get("/{id}", response_model=TourModel)
async def get_tour(id: int):
    tour = await tours_collection.find_one({"id": id})
    if tour:
        return TourModel(**tour)
    raise HTTPException(status_code=404, detail="Tour not found")

@router.post("/", response_model=TourModel)
async def create_tour(tour: TourModel = Body(...)):
    tour_dict = tour.dict()
    await tours_collection.insert_one(tour_dict)
    return tour

@router.put("/{id}", response_model=TourModel)
async def update_tour(id: int, tour: TourModel = Body(...)):
    updated_tour = await tours_collection.find_one_and_update(
        {"id": id},
        {"$set": tour.dict()}
    )
    if updated_tour:
        return tour
    raise HTTPException(status_code=404, detail="Tour not found")

@router.delete("/{id}")
async def delete_tour(id: int):
    delete_result = await tours_collection.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return {"message": "Tour deleted successfully"}
    raise HTTPException(status_code=404, detail="Tour not found")
