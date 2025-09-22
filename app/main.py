from fastapi import FastAPI, HTTPException
from typing import List
from app.database import Database, get_pet_profiles_collection, get_products_collection
from app.models.pet import PetProfile, PetProfileResponse
from app.services.safety_filter import SafetyFilter
from bson import ObjectId


app = FastAPI(title="Pet Product Recommendation API", version="1.0.0")

@app.on_event("startup")
def startup_db_client():
    Database.initialize()

@app.on_event("shutdown")
def shutdown_db_client():
    Database.close_connection()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pet Product Recommendation System!"}


@app.post("/recommendations/{pet_id}", response_model=dict)
def get_recommendations(pet_id: str):
    """
    Get product recommendations for a specific pet.
    """
    pets_collection = get_pet_profiles_collection()
    products_collection = get_products_collection()

    pet_data = pets_collection.find_one({"pet_id": pet_id})

    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")

    pet = PetProfile(**pet_data)

    all_products = list(products_collection.find({}))

    safe_products = SafetyFilter.filter_products_for_pet(pet, all_products)

    
    for product in safe_products:
        if '_id' in product and isinstance(product['_id'], ObjectId):
            product['_id'] = str(product['_id'])


    return {"pet": PetProfileResponse(**pet.dict()), "recommendations": safe_products}



@app.post("/pets/", response_model=PetProfileResponse)
def create_pet_profile(pet: PetProfile):
    """
    Create a new pet profile.
    """
    pets_collection = get_pet_profiles_collection()
    pet_dict = pet.dict()
    result = pets_collection.insert_one(pet_dict)
    created_pet = pets_collection.find_one({"_id": result.inserted_id})
    return PetProfileResponse(**created_pet)


@app.get("/pets/{pet_id}", response_model=PetProfileResponse)
def get_pet_profile(pet_id: str):
    """
    Get a pet profile by pet_id.
    """
    pets_collection = get_pet_profiles_collection()
    pet_data = pets_collection.find_one({"pet_id": pet_id})
    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    return PetProfileResponse(**pet_data)


@app.put("/pets/{pet_id}", response_model=PetProfileResponse)
def update_pet_profile(pet_id: str, pet: PetProfile):
    """
    Update a pet profile.
    """
    pets_collection = get_pet_profiles_collection()
    pet_dict = pet.dict()
    result = pets_collection.update_one({"pet_id": pet_id}, {"$set": pet_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    updated_pet = pets_collection.find_one({"pet_id": pet_id})
    return PetProfileResponse(**updated_pet)


@app.delete("/pets/{pet_id}", response_model=dict)
def delete_pet_profile(pet_id: str):
    """
    Delete a pet profile.
    """
    pets_collection = get_pet_profiles_collection()
    result = pets_collection.delete_one({"pet_id": pet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    return {"message": f"Pet with ID {pet_id} deleted successfully"}