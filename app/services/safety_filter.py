from typing import List, Dict, Any
from app.models.pet import PetProfile

class SafetyFilter:
    """Safety filtering service to ensure pet-products compatibility"""
    
    @staticmethod
    def is_product_safe_for_pet(pet: PetProfile, product: Dict[str, Any]) -> bool:
        """Check if a product is safe for a specific pet Returns True if safe , False if unsafe"""
        
        if not SafetyFilter._check_age_compatibility(pet, product):
            return False
        
        if not SafetyFilter._check_allergies(pet, product):
            return False
        
        if not SafetyFilter._check_health_conditions(pet, product):
            return False
        
        if not SafetyFilter._check_species_compatibility(pet, product):
            return False
        
        return True
    
    @staticmethod 
    def _check_age_compatibility(pet: PetProfile, product: Dict[str, Any]) -> bool:
        """Check if product age group matches pet age group"""
        product_age_groups = product.get("age_groups", [])
        pet_age_group = pet.age_group.lower()
        
        if not product_age_groups:
            return True
        
        for allowed_age in product_age_groups:
            if allowed_age.lower() == pet_age_group:
                return True
            
        return False
    
    @staticmethod
    def _check_allergies(pet: PetProfile, product: Dict[str, Any]) -> bool:
        """Check if product ingredients conflict with pet known allergies"""
        pet_allergies = [allergy.lower().strip() for allergy in pet.known_allergies]
        
        if not pet_allergies:
            return True
        
        product_ingredients = product.get("ingredients", [])
        for ingredient in product_ingredients:
            ingredient_lower = ingredient.lower().strip()
            for allergy in pet_allergies:
                if allergy in ingredient_lower:
                    return False
                
        product_tags = product.get("tags", [])
        for tag in product_tags:
            tag_lower = tag.lower().strip()
            for allergy in pet_allergies:
                if allergy in tag_lower:
                    return False
                
        return True
    
    @staticmethod
    def _check_health_conditions(pet: PetProfile, product: Dict[str, Any]) -> bool:
        """Check if product is suitable for pet's health conditions""" 
        pet_conditions = [condition.lower().strip() for condition in pet.health_conditions]  
        
        if not pet_conditions:
            return True
        
        product_warnings = product.get("safety", {}).get("health_warnings", [])
        for warning in product_warnings:
            warning_lower = warning.lower().strip()
            for condition in pet_conditions:
                if condition in warning_lower:
                    return False
     
        return True 
    
    @staticmethod
    def _check_species_compatibility(pet: PetProfile, product: Dict[str, Any]) -> bool:
        """Check if product is intended for pet's species/category"""
        product_category = pet.category.lower().strip()
        product_pet_type = product.get("pet_type", "").lower().strip()
        
        if not product_pet_type:
            return True
        
            
        return product_category == product_pet_type
    
    @staticmethod
    def filter_products_for_pet(pet: PetProfile, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter a list of products to only those safe for the given pet"""
        safe_products = []
        for product in products:
            if SafetyFilter.is_product_safe_for_pet(pet, product):
                safe_products.append(product)
        return safe_products
                    
    @staticmethod
    def get_safety_reasons(pet: PetProfile, product: Dict[str, Any]) -> List[str]:
        """Get List of reasons why a product might not be safe for a pet"""
        
        reasons =[]
        
        if not SafetyFilter._check_age_compatibility(pet, product):
            product_ages = product.get("age_group", [])
            reasons.append(f"Age mismatch: Pet is {pet.age_group}, product is for {product_ages}")
        
        if not SafetyFilter._check_allergies(pet, product):
            reasons.append(f"Contains allergens: Pet allergic to {pet.known_allergies}")
            
        if not SafetyFilter._check_health_conditions(pet, product):
            reasons.append(f"Health condition conflict: Pet has {pet.health_conditions}") 
            
        if not SafetyFilter._check_species_compatibility(pet, product):
            reasons.append(f"Species mismatch: Pet is {pet.category}, product is for {product.get('pet_type')}")

        return reasons
