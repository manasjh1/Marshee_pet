from typing import List, Dict , Any , Tuple
from app.models.pet import PetProfile
from app.services.safety_filter import SafetyFilter
from collections import Counter
import math

class BalancedRecommendationEngine:
    """Balanced recommendation engine with health-safety priority """
    
    WEIGHTS = {
        'health_condition_match': 0.35,
        'safety_allergy_match': 0.30,
        'general_compatibility' : 0.25,
        'quality_business': 0.10
    }
    
    HEALTH_CONDITION_MAPPING = {
        'arthritis': ['joint support', 'joint care', 'mobility', 'glucosamine', 'anti-inflammatory'],
        'joint issues': ['joint support', 'joint care', 'mobility', 'glucosamine'],
        'hip dysplasia': ['joint support', 'joint care', 'hip health', 'mobility'],
        'dental issues': ['dental care', 'dental health', 'tartar control', 'oral health'],
        'dental problems': ['dental care', 'dental health', 'tartar control'],
        'skin issues': ['skin health', 'omega-3', 'coat care', 'skin support'],
        'skin problems': ['skin health', 'omega-3', 'coat care'],
        'digestive issues': ['digestive health', 'probiotics', 'easy digest', 'sensitive stomach'],
        'sensitive stomach': ['digestive health', 'gentle', 'easy digest', 'sensitive'],
        'kidney disease': ['kidney support', 'renal', 'low phosphorus'],
        'heart disease': ['heart health', 'cardiac', 'low sodium'],
        'diabetes': ['diabetic', 'low sugar', 'blood sugar control'],
        'obesity': ['weight management', 'weight control', 'low calorie', 'light'],
        'overweight': ['weight management', 'weight control', 'low calorie'],
        'allergies': ['hypoallergenic', 'limited ingredient', 'allergy relief']
        
    }
    
    AGE_GROUP_NEEDS = {
        'puppy': ['growth', 'development', 'puppy formula', 'high energy', 'immunity'],
        'kitten': ['growth', 'development', 'kitten formula', 'high energy'],
        'adult': ['maintenance', 'adult formula', 'balanced nutrition'],
        'senior': ['senior care', 'senior formula', 'joint support', 'easy digest', 'cognitive support']
    }
    
    BREED_SIZE_MAPPING = {
        'chihuahua': 'small',
        'pomeranian': 'small', 
        'yorkshire terrier': 'small',
        'maltese': 'small',
        'pug': 'medium',
        'beagle': 'medium',
        'cocker spaniel': 'medium',
        'labrador': 'large',
        'golden retriever': 'large',
        'german shepherd': 'large',
        'rottweiler': 'large'
    }
    
    @classmethod
    def generate_recommendations(cls, pet: PetProfile, products: List[Dict[str, Any]], 
                               limit: int = 10) -> List[Dict[str, Any]]:
        """Generate balanced recommendations using Option 1 weights"""
        
        print(f"Generating recommendations for {pet.name} using balanced health-first approach")
        
        # Safety filtering first (absolute requirement)
        safe_products = SafetyFilter.filter_products_for_pet(pet, products)
        print(f"Safe products: {len(safe_products)}/{len(products)}")
        
        if not safe_products:
            return []
        
        # Generate pet analysis
        pet_analysis = cls._analyze_pet_profile(pet)
        print(f"Pet analysis complete: {len(pet_analysis['health_needs'])} health needs identified")
        
        # Score each safe product
        scored_products = []
        for product in safe_products:
            score_data = cls._calculate_balanced_score(pet, product, pet_analysis)
            
            product_copy = product.copy()
            product_copy['recommendation_score'] = score_data['total_score']
            product_copy['recommendation_reasons'] = score_data['reasons']
            product_copy['score_breakdown'] = score_data['breakdown']
            
            scored_products.append(product_copy)
        
        # Sort by score and optimize
        scored_products.sort(key=lambda x: x['recommendation_score'], reverse=True)
        optimized_products = cls._optimize_results(scored_products, pet_analysis)
        
        return optimized_products[:limit]
    
    @classmethod
    def _analyze_pet_profile(cls, pet: PetProfile) -> Dict[str, Any]:
        """Analyze pet profile and extract key matching criteria"""
        
        analysis = {
            'health_needs': [],
            'safety_requirements': [],
            'age_needs': [],
            'breed_considerations': [],
            'general_tags': []
        }
        
        # Health condition analysis
        for condition in pet.health_conditions:
            condition_lower = condition.lower().strip()
            for health_key, benefits in cls.HEALTH_CONDITION_MAPPING.items():
                if health_key in condition_lower:
                    analysis['health_needs'].extend(benefits)
                    break
            else:
                # If no specific mapping, add the condition itself as a need
                analysis['health_needs'].append(condition_lower)
        
        # Safety requirements from allergies
        for allergy in pet.known_allergies:
            allergy_lower = allergy.lower().strip()
            if 'grain' in allergy_lower:
                analysis['safety_requirements'].extend(['grain-free', 'gluten-free'])
            elif 'chicken' in allergy_lower:
                analysis['safety_requirements'].extend(['chicken-free', 'alternative protein'])
            elif 'beef' in allergy_lower:
                analysis['safety_requirements'].extend(['beef-free', 'alternative protein'])
            elif 'dairy' in allergy_lower:
                analysis['safety_requirements'].extend(['dairy-free', 'lactose-free'])
            
            # Always add hypoallergenic for any food allergy
            analysis['safety_requirements'].append('hypoallergenic')
        
        # Age-specific needs
        age_group = pet.age_group.lower()
        if age_group in cls.AGE_GROUP_NEEDS:
            analysis['age_needs'].extend(cls.AGE_GROUP_NEEDS[age_group])
        
        # Breed considerations
        if pet.breed:
            breed_lower = pet.breed.lower()
            # Size-based needs
            for breed_name, size in cls.BREED_SIZE_MAPPING.items():
                if breed_name in breed_lower:
                    analysis['breed_considerations'].append(f"{size} breed")
                    break
            
            # Add the breed itself
            analysis['breed_considerations'].append(breed_lower)
        
        # General demographic tags
        analysis['general_tags'].extend([
            pet.category.lower(),
            pet.age_group.lower(),
            pet.gender.lower() if pet.gender else ''
        ])
        
        # Remove duplicates and empty strings
        for key in analysis:
            analysis[key] = list(set([item for item in analysis[key] if item]))
        
        return analysis
    
    @classmethod
    def _calculate_balanced_score(cls, pet: PetProfile, product: Dict[str, Any], 
                                pet_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate score using Option 1 balanced weights"""
        
        scores = {
            'health_condition_match': 0.0,
            'safety_allergy_match': 0.0,
            'general_compatibility': 0.0,
            'quality_business': 0.0
        }
        
        reasons = []
        
        # 1. Health Condition Match (35%)
        health_score_data = cls._calculate_health_condition_score(
            pet_analysis['health_needs'], product
        )
        scores['health_condition_match'] = health_score_data['score']
        reasons.extend(health_score_data['reasons'])
        
        # 2. Safety & Allergy Match (30%)
        safety_score_data = cls._calculate_safety_allergy_score(
            pet, pet_analysis['safety_requirements'], product
        )
        scores['safety_allergy_match'] = safety_score_data['score']
        reasons.extend(safety_score_data['reasons'])
        
        # 3. General Compatibility (25%)
        compatibility_score_data = cls._calculate_general_compatibility_score(
            pet, pet_analysis, product
        )
        scores['general_compatibility'] = compatibility_score_data['score']
        reasons.extend(compatibility_score_data['reasons'])
        
        # 4. Quality & Business (10%)
        quality_score = cls._calculate_quality_business_score(product)
        scores['quality_business'] = quality_score
        if quality_score > 0.8:
            reasons.append("High-quality product with excellent ratings")
        elif quality_score > 0.6:
            reasons.append("Well-rated product")
        
        # Calculate weighted total
        total_score = sum(scores[key] * cls.WEIGHTS[key] for key in scores.keys())
        
        return {
            'total_score': round(total_score, 3),
            'breakdown': scores,
            'reasons': reasons[:5]  # Limit to top 5 reasons
        }
        
    @classmethod
    def _calculate_health_condition_score(cls, health_needs: List[str], 
                                        product: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate health condition matching score"""
        
        if not health_needs:
            return {'score': 0.5, 'reasons': ['No specific health needs identified']}
        
        # Collect all product text for searching
        product_tags = [tag.lower() for tag in product.get('tags', [])]
        product_name = product.get('name', '').lower()
        product_description = product.get('description', '').lower()
        
        all_product_text = product_tags + [product_name, product_description]
        
        matches = 0
        matched_needs = []
        
        for need in health_needs:
            need_lower = need.lower()
            # Check if any product text contains this health need
            if any(need_lower in text for text in all_product_text):
                matches += 1
                matched_needs.append(need)
        
        # Calculate score
        score = matches / len(health_needs) if health_needs else 0
        
        # Create reasons
        reasons = []
        if matched_needs:
            reasons.extend([f"Addresses {need}" for need in matched_needs[:3]])
        else:
            reasons.append("No specific health condition matches found")
        
        return {
            'score': min(score, 1.0),
            'reasons': reasons
        }
        
        
    @classmethod
    def _calculate_safety_allergy_score(cls, pet: PetProfile, safety_requirements: List[str],
                                      product: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate safety and allergy compatibility score"""
        
        # Base score for passing safety filter
        score = 0.8
        reasons = ["Passes all safety requirements"]
        
        # Check age group compatibility
        pet_age = pet.age_group.lower()
        product_age_groups = [age.lower() for age in product.get('age_group', [])]
        
        if pet_age in product_age_groups:
            score += 0.1
            reasons.append(f"Perfect age match for {pet_age}")
        elif not product_age_groups:  # No age restriction
            score += 0.05
        
        # Check safety requirements fulfillment
        if safety_requirements:
            product_tags = [tag.lower() for tag in product.get('tags', [])]
            product_name = product.get('name', '').lower()
            
            safety_matches = 0
            for requirement in safety_requirements:
                req_lower = requirement.lower()
                if (any(req_lower in tag for tag in product_tags) or 
                    req_lower in product_name):
                    safety_matches += 1
                    if safety_matches <= 2:  # Limit reasons
                        reasons.append(f"Meets safety requirement: {requirement}")
            
            # Bonus for meeting safety requirements
            if safety_matches > 0:
                safety_bonus = min(safety_matches / len(safety_requirements) * 0.1, 0.1)
                score += safety_bonus
        
        return {
            'score': min(score, 1.0),
            'reasons': reasons[:3]
        }
        
        
    @classmethod
    def _calculate_general_compatibility_score(cls, pet: PetProfile, pet_analysis: Dict[str, Any],
                                             product: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate general compatibility score"""
        
        score = 0.0
        reasons = []
        
        # Pet type matching (most important for general compatibility)
        if pet.category.lower() == product.get('pet_type', '').lower():
            score += 0.4
            reasons.append(f"Perfect species match for {pet.category}")
        
        # Tag matching
        all_pet_tags = (pet_analysis['age_needs'] + 
                       pet_analysis['breed_considerations'] + 
                       pet_analysis['general_tags'])
        
        product_tags = [tag.lower() for tag in product.get('tags', [])]
        
        if all_pet_tags and product_tags:
            tag_matches = set([tag.lower() for tag in all_pet_tags]) & set(product_tags)
            if tag_matches:
                tag_score = len(tag_matches) / len(all_pet_tags)
                score += tag_score * 0.4
                reasons.append(f"Good tag compatibility ({len(tag_matches)} matches)")
        
        # Breed size compatibility
        if pet.breed:
            breed_lower = pet.breed.lower()
            product_breed_sizes = [size.lower() for size in product.get('breed_size', [])]
            
            # Check if "All Breed Sizes" is included
            if any('all' in size for size in product_breed_sizes):
                score += 0.1
                reasons.append("Suitable for all breed sizes")
            else:
                # Check specific size compatibility
                pet_size = None
                for breed_name, size in cls.BREED_SIZE_MAPPING.items():
                    if breed_name in breed_lower:
                        pet_size = size
                        break
                
                if pet_size and any(pet_size in size for size in product_breed_sizes):
                    score += 0.1
                    reasons.append(f"Perfect size match for {pet_size} breed")
        
        # Category matching
        pet_category = pet.category.lower()
        product_category = product.get('category', '').lower()
        if 'food' in product_category and pet_category in ['dog', 'cat']:
            score += 0.1
            reasons.append("Appropriate food category")
        
        return {
            'score': min(score, 1.0),
            'reasons': reasons[:3]
        }
        
    @classmethod
    def _calculate_quality_business_score(cls, product: Dict[str, Any]) -> float:
        """Calculate quality and business metrics score"""
        
        score = 0.0
        business_data = product.get('business_data', {})
        
        if isinstance(business_data, dict):
            # Rating component (0-5 scale)
            avg_rating = business_data.get('avg_rating', 0)
            if avg_rating > 0:
                score += (avg_rating / 5.0) * 0.5
            
            # Review count (trust factor)
            total_reviews = business_data.get('total_reviews', 0)
            if total_reviews >= 10:
                score += 0.2
            elif total_reviews >= 5:
                score += 0.1
            
            # Popularity score
            popularity = business_data.get('popularity_score', 0)
            if popularity > 0:
                score += min(popularity / 100.0, 0.3)
            
            # Premium product bonus
            if business_data.get('is_premium', False):
                score += 0.1
        
        # Brand trust (based on your schema)
        brand = product.get('brand', '').lower()
        trusted_brands = ['paws for greens', 'royal canin', 'hills', 'purina']
        if any(trusted in brand for trusted in trusted_brands):
            score += 0.1
        
        return min(score, 1.0)
    
    @classmethod
    def _optimize_results(cls, scored_products: List[Dict[str, Any]], 
                         pet_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize results for diversity while maintaining health priority"""
        
        if not scored_products:
            return []
        
        optimized = []
        seen_brands = set()
        seen_categories = set()
        
        # Prioritize products with health matches
        health_products = [p for p in scored_products 
                          if p['score_breakdown']['health_condition_match'] > 0.3]
        regular_products = [p for p in scored_products 
                           if p['score_breakdown']['health_condition_match'] <= 0.3]
        
        # Add health products first (up to 60% of results)
        health_limit = max(6, int(len(scored_products) * 0.6))
        for product in health_products[:health_limit]:
            brand = product.get('brand', '').lower()
            category = product.get('category', '').lower()
            
            # Limit brand diversity (max 2 per brand)
            brand_count = sum(1 for p in optimized if p.get('brand', '').lower() == brand)
            if brand_count < 2:
                optimized.append(product)
                seen_brands.add(brand)
                seen_categories.add(category)
        
        # Fill remaining slots with regular products
        remaining_slots = 10 - len(optimized)
        for product in regular_products[:remaining_slots]:
            optimized.append(product)
        
        return optimized                
        