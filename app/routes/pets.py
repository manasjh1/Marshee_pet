from fastapi import APIRouter, HTTPException
from app.database import get_pet_profiles_collection
from app.models.pet import PetProfile, PetProfileResponse
from app.services.recommendation import BalancedRecommendationEngine
from bson import ObjectId

router = APIRouter(prefix="/pets", tags=["pets"])

@router.post("/", response_model=PetProfileResponse)
def create_pet_profile(pet: PetProfile):
    """Create a new pet profile."""
    pets_collection = get_pet_profiles_collection()
    pet_dict = pet.dict()
    result = pets_collection.insert_one(pet_dict)
    created_pet = pets_collection.find_one({"_id": result.inserted_id})
    return PetProfileResponse(**created_pet)

@router.get("/{pet_id}", response_model=PetProfileResponse)
def get_pet_profile(pet_id: str):
    """Get a pet profile by pet_id."""
    pets_collection = get_pet_profiles_collection()
    pet_data = pets_collection.find_one({"pet_id": pet_id})
    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    return PetProfileResponse(**pet_data)

@router.put("/{pet_id}", response_model=PetProfileResponse)
def update_pet_profile(pet_id: str, pet: PetProfile):
    """Update a pet profile."""
    pets_collection = get_pet_profiles_collection()
    pet_dict = pet.dict()
    result = pets_collection.update_one({"pet_id": pet_id}, {"$set": pet_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    updated_pet = pets_collection.find_one({"pet_id": pet_id})
    return PetProfileResponse(**updated_pet)

@router.delete("/{pet_id}")
def delete_pet_profile(pet_id: str):
    """Delete a pet profile."""
    pets_collection = get_pet_profiles_collection()
    result = pets_collection.delete_one({"pet_id": pet_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")
    return {"message": f"Pet with ID {pet_id} deleted successfully"}

@router.get("/{pet_id}/health-analysis")
def analyze_pet_health_profile(pet_id: str):
    """
    Analyze a pet's health profile and show how it affects recommendations.
    """
    pets_collection = get_pet_profiles_collection()
    
    pet_data = pets_collection.find_one({"pet_id": pet_id})
    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")

    pet = PetProfile(**pet_data)
    pet_analysis = BalancedRecommendationEngine._analyze_pet_profile(pet)

    # Calculate health complexity score
    health_complexity = len(pet.health_conditions) * 2 + len(pet.known_allergies) * 3
    
    if health_complexity >= 8:
        complexity_level = "High"
        complexity_description = "Multiple health conditions and allergies require careful product selection"
    elif health_complexity >= 4:
        complexity_level = "Medium" 
        complexity_description = "Some health considerations need attention in product selection"
    elif health_complexity >= 1:
        complexity_level = "Low"
        complexity_description = "Minimal health restrictions with some considerations"
    else:
        complexity_level = "None"
        complexity_description = "No specific health restrictions identified"

    return {
        "pet": PetProfileResponse(**pet.dict()),
        "health_analysis": {
            "health_needs_identified": pet_analysis["health_needs"],
            "safety_requirements": pet_analysis["safety_requirements"],
            "age_related_needs": pet_analysis["age_needs"],
            "breed_considerations": pet_analysis["breed_considerations"],
            "complexity_level": complexity_level,
            "complexity_description": complexity_description,
            "health_complexity_score": health_complexity
        },
        "recommendation_impact": {
            "health_condition_weight": "35%",
            "safety_allergy_weight": "30%",
            "prioritizes_health_products": len(pet.health_conditions) > 0,
            "requires_allergy_filtering": len(pet.known_allergies) > 0,
            "age_specific_needs": pet.age_group.lower() in ['puppy', 'kitten', 'senior']
        }
    }