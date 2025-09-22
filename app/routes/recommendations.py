from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.database import get_pet_profiles_collection, get_products_collection
from app.models.pet import PetProfile, PetProfileResponse
from app.services.safety_filter import SafetyFilter
from app.services.recommendation import BalancedRecommendationEngine
from bson import ObjectId

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/{pet_id}")
def get_balanced_recommendations(
    pet_id: str,
    limit: int = Query(default=10, ge=1, le=50, description="Number of recommendations"),
    include_scores: bool = Query(default=False, description="Include detailed scoring breakdown"),
    min_score: float = Query(default=0.0, ge=0.0, le=1.0, description="Minimum recommendation score")
):
    """
    Get balanced health-first product recommendations.
    
    Scoring Breakdown:
    - Health Condition Match: 35% (addresses specific health needs)
    - Safety & Allergy Match: 30% (safe for pet's allergies and age)
    - General Compatibility: 25% (species, breed, lifestyle match)
    - Quality & Business: 10% (ratings, reviews, popularity)
    """
    pets_collection = get_pet_profiles_collection()
    products_collection = get_products_collection()

    # Get pet profile
    pet_data = pets_collection.find_one({"pet_id": pet_id})
    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")

    pet = PetProfile(**pet_data)

    # Get all products
    all_products = list(products_collection.find({}))
    for product in all_products:
        if '_id' in product and isinstance(product['_id'], ObjectId):
            product['_id'] = str(product['_id'])

    # Generate balanced recommendations
    recommendations = BalancedRecommendationEngine.generate_recommendations(
        pet=pet, 
        products=all_products, 
        limit=limit
    )

    # Filter by minimum score if specified
    if min_score > 0:
        recommendations = [r for r in recommendations if r.get('recommendation_score', 0) >= min_score]

    # Analyze recommendation quality
    health_focused_count = sum(1 for r in recommendations 
                              if r.get('score_breakdown', {}).get('health_condition_match', 0) > 0.3)

    # Prepare response
    response_data = {
        "pet": PetProfileResponse(**pet.dict()),
        "recommendations": recommendations,
        "analysis": {
            "total_products_checked": len(all_products),
            "safe_products_found": len(SafetyFilter.filter_products_for_pet(pet, all_products)),
            "recommendations_returned": len(recommendations),
            "health_focused_products": health_focused_count,
            "has_health_conditions": len(pet.health_conditions) > 0,
            "has_allergies": len(pet.known_allergies) > 0,
            "algorithm_version": "balanced_health_first_v3"
        }
    }

    # Optionally remove detailed scoring for cleaner response
    if not include_scores:
        for rec in response_data["recommendations"]:
            rec.pop("score_breakdown", None)

    return response_data

@router.get("/{pet_id}/explain/{product_id}")
def explain_balanced_recommendation(pet_id: str, product_id: str):
    """
    Explain why a specific product was recommended using the balanced scoring system.
    """
    pets_collection = get_pet_profiles_collection()
    products_collection = get_products_collection()

    # Get pet and product
    pet_data = pets_collection.find_one({"pet_id": pet_id})
    if not pet_data:
        raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")

    product_data = products_collection.find_one({"product_id": product_id})
    if not product_data:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    pet = PetProfile(**pet_data)
    
    # Convert ObjectId
    if '_id' in product_data and isinstance(product_data['_id'], ObjectId):
        product_data['_id'] = str(product_data['_id'])

    # Check safety first
    is_safe = SafetyFilter.is_product_safe_for_pet(pet, product_data)
    
    if not is_safe:
        safety_reasons = SafetyFilter.get_safety_reasons(pet, product_data)
        return {
            "pet_id": pet_id,
            "pet_name": pet.name,
            "product_id": product_id,
            "product_name": product_data.get("name", "Unknown"),
            "is_recommended": False,
            "reason": "Safety concerns prevent recommendation",
            "safety_issues": safety_reasons,
            "explanation": "This product cannot be recommended due to safety concerns. Safety is always our top priority."
        }

    # Get detailed scoring
    pet_analysis = BalancedRecommendationEngine._analyze_pet_profile(pet)
    score_data = BalancedRecommendationEngine._calculate_balanced_score(pet, product_data, pet_analysis)

    # Determine recommendation level
    score = score_data["total_score"]
    if score >= 0.8:
        recommendation_level = "Highly Recommended"
    elif score >= 0.6:
        recommendation_level = "Recommended"
    elif score >= 0.4:
        recommendation_level = "Moderately Suitable"
    elif score >= 0.2:
        recommendation_level = "Somewhat Suitable"
    else:
        recommendation_level = "Not Strongly Recommended"

    return {
        "pet_id": pet_id,
        "pet_name": pet.name,
        "product_id": product_id,
        "product_name": product_data.get("name", "Unknown"),
        "is_safe": True,
        "overall_score": score,
        "recommendation_level": recommendation_level,
        "score_breakdown": score_data["breakdown"],
        "reasons": score_data["reasons"],
        "detailed_analysis": {
            "pet_health_needs": pet_analysis["health_needs"],
            "pet_safety_requirements": pet_analysis["safety_requirements"],
            "pet_age_needs": pet_analysis["age_needs"],
            "pet_breed_considerations": pet_analysis["breed_considerations"],
            "scoring_weights": BalancedRecommendationEngine.WEIGHTS
        },
        "explanation": f"This product scored {score:.2f}/1.0 and is {recommendation_level.lower()} for {pet.name}. The balanced scoring considers health needs (35%), safety compatibility (30%), general compatibility (25%), and quality metrics (10%)."
    }