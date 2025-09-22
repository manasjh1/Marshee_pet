from typing import List, Dict, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import re

class MLTagGenerator:
    """ML-based tag generation using sentence embeddings"""
    
    def __init__(self):
        print("Loading ML tag generation model...")
        # Load lightweight, fast model (22MB)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tag_database = self._initialize_tag_database()
        print("ML tag generation model loaded successfully!")
    
    def _initialize_tag_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive tag database with embeddings"""
        
        # Comprehensive tag definitions by category
        tag_definitions = {
            # Health & Medical Tags (High Priority)
            "joint-support": {
                "text": "joint support arthritis hip dysplasia mobility glucosamine chondroitin",
                "categories": ["food", "supplement", "bed", "medicine"],
                "importance": "high"
            },
            "digestive-health": {
                "text": "digestive health probiotic prebiotic stomach intestinal gut sensitive",
                "categories": ["food", "supplement", "medicine"],
                "importance": "high"
            },
            "skin-health": {
                "text": "skin health coat care omega fatty acid dermatitis itchy allergies",
                "categories": ["food", "supplement", "grooming", "medicine"],
                "importance": "high"
            },
            "dental-care": {
                "text": "dental care teeth cleaning tartar plaque breath oral hygiene",
                "categories": ["food", "treats", "toys", "medicine"],
                "importance": "medium"
            },
            "heart-health": {
                "text": "heart health cardiac cardiovascular taurine circulation",
                "categories": ["food", "supplement", "medicine"],
                "importance": "high"
            },
            "kidney-support": {
                "text": "kidney support renal urinary bladder phosphorus protein restriction",
                "categories": ["food", "supplement", "medicine"],
                "importance": "high"
            },
            "weight-management": {
                "text": "weight management diet light low calorie obesity overweight slim",
                "categories": ["food", "supplement"],
                "importance": "medium"
            },
            "senior-care": {
                "text": "senior care elderly mature aged old cognitive brain support",
                "categories": ["food", "supplement", "bed", "medicine"],
                "importance": "medium"
            },
            
            # Life Stage Tags
            "puppy-formula": {
                "text": "puppy growth development young baby small breed large breed",
                "categories": ["food", "supplement"],
                "importance": "medium"
            },
            "adult-maintenance": {
                "text": "adult maintenance balanced nutrition everyday regular",
                "categories": ["food"],
                "importance": "low"
            },
            "kitten-formula": {
                "text": "kitten growth development young baby feline cat",
                "categories": ["food", "supplement"],
                "importance": "medium"
            },
            
            # Dietary & Nutrition Tags
            "grain-free": {
                "text": "grain free gluten free wheat corn rice barley oats",
                "categories": ["food", "treats"],
                "importance": "medium"
            },
            "high-protein": {
                "text": "high protein meat fish chicken beef lamb turkey",
                "categories": ["food", "treats"],
                "importance": "low"
            },
            "plant-based": {
                "text": "plant based vegan vegetarian pea protein potato protein",
                "categories": ["food", "treats"],
                "importance": "low"
            },
            "limited-ingredient": {
                "text": "limited ingredient simple hypoallergenic sensitive allergies",
                "categories": ["food", "treats"],
                "importance": "medium"
            },
            "natural": {
                "text": "natural organic wholesome pure clean",
                "categories": ["food", "treats", "grooming"],
                "importance": "low"
            },
            
            # Quality & Safety Tags
            "organic": {
                "text": "organic natural certified pesticide free chemical free",
                "categories": ["food", "treats", "grooming"],
                "importance": "low"
            },
            "vet-formulated": {
                "text": "veterinarian formulated approved recommended medical prescription",
                "categories": ["food", "supplement", "medicine"],
                "importance": "high"
            },
            "hypoallergenic": {
                "text": "hypoallergenic allergy friendly sensitive skin food allergies",
                "categories": ["food", "treats", "grooming", "bed"],
                "importance": "medium"
            },
            "premium": {
                "text": "premium high quality superior grade excellent",
                "categories": ["food", "treats", "toys", "bed"],
                "importance": "low"
            },
            
            # Toy Tags
            "interactive": {
                "text": "interactive puzzle mental stimulation brain training smart",
                "categories": ["toys"],
                "importance": "medium"
            },
            "chew-toy": {
                "text": "chew toy dental teething aggressive chewer durable tough",
                "categories": ["toys"],
                "importance": "medium"
            },
            "squeaky": {
                "text": "squeaky noise sound play fun entertainment",
                "categories": ["toys"],
                "importance": "low"
            },
            "puzzle-toy": {
                "text": "puzzle toy brain game challenge problem solving",
                "categories": ["toys"],
                "importance": "medium"
            },
            "plush-toy": {
                "text": "plush soft stuffed cuddle comfort gentle",
                "categories": ["toys"],
                "importance": "low"
            },
            
            # Bed & Comfort Tags
            "orthopedic": {
                "text": "orthopedic therapeutic medical support joint relief pressure",
                "categories": ["bed", "accessories"],
                "importance": "high"
            },
            "memory-foam": {
                "text": "memory foam comfort cushioning support pressure relief",
                "categories": ["bed"],
                "importance": "medium"
            },
            "waterproof": {
                "text": "waterproof water resistant washable easy clean",
                "categories": ["bed", "accessories"],
                "importance": "low"
            },
            "cooling": {
                "text": "cooling gel temperature regulation hot weather summer",
                "categories": ["bed", "accessories"],
                "importance": "low"
            },
            
            # Size Tags
            "small-breed": {
                "text": "small breed tiny toy miniature chihuahua yorkie pomeranian",
                "categories": ["food", "bed", "accessories", "toys"],
                "importance": "medium"
            },
            "large-breed": {
                "text": "large breed big giant labrador retriever german shepherd",
                "categories": ["food", "bed", "accessories", "toys"],
                "importance": "medium"
            },
            "medium-breed": {
                "text": "medium breed moderate size beagle bulldog cocker spaniel",
                "categories": ["food", "bed", "accessories"],
                "importance": "medium"
            },
            
            # Grooming Tags
            "shampoo": {
                "text": "shampoo cleaning washing bathing soap gentle mild",
                "categories": ["grooming"],
                "importance": "medium"
            },
            "flea-tick": {
                "text": "flea tick prevention parasite insect repellent protection",
                "categories": ["grooming", "medicine"],
                "importance": "high"
            }
        }
        
        # Generate embeddings for all tags
        print("Generating tag embeddings...")
        tag_database = {}
        for tag_name, tag_info in tag_definitions.items():
            embedding = self.model.encode(tag_info["text"])
            tag_database[tag_name] = {
                "embedding": embedding,
                "categories": tag_info["categories"],
                "importance": tag_info["importance"]
            }
        
        return tag_database
    
    def generate_tags(self, product_data: Dict[str, Any]) -> List[str]:
        """Generate tags using ML embeddings"""
        
        # Extract and combine product text
        product_text = self._extract_product_text(product_data)
        product_category = product_data.get('category', '').lower()
        
        # Generate product embedding
        product_embedding = self.model.encode(product_text)
        
        # Calculate similarities with all tags
        tag_scores = []
        
        for tag_name, tag_info in self.tag_database.items():
            # Check if tag is relevant for this product category
            if product_category:
                category_match = False
                for cat in tag_info["categories"]:
                    if cat in product_category or product_category in cat:
                        category_match = True
                        break
                if not category_match:
                    continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(product_embedding, tag_info["embedding"])
            
            # Apply importance weighting
            importance_weight = self._get_importance_weight(tag_info["importance"])
            weighted_score = similarity * importance_weight
            
            tag_scores.append((tag_name, weighted_score, similarity))
        
        # Select tags based on threshold and ranking
        selected_tags = self._select_best_tags(tag_scores)
        
        # Add basic categorical tags
        basic_tags = self._add_basic_tags(product_data)
        
        # Combine and clean
        all_tags = selected_tags + basic_tags
        return self._clean_tags(list(set(all_tags)))
    
    def _extract_product_text(self, product_data: Dict[str, Any]) -> str:
        """Extract and combine relevant text from product data"""
        
        text_parts = []
        
        # Primary text sources
        name = product_data.get('name', '')
        description = product_data.get('description', '')
        category = product_data.get('category', '')
        sub_category = product_data.get('sub_category', '')
        product_type = product_data.get('Product_type', '')
        
        text_parts.extend([name, description, category, sub_category, product_type])
        
        # Ingredients (for food products)
        ingredients = product_data.get('ingredients', [])
        if ingredients:
            text_parts.append(' '.join(ingredients))
        
        # Age groups
        age_groups = product_data.get('age_group', [])
        if age_groups:
            text_parts.append(' '.join(age_groups))
        
        # Safety information
        safety_info = product_data.get('safety', {})
        if isinstance(safety_info, dict):
            age_restrictions = safety_info.get('age_restrictions', '')
            if age_restrictions:
                text_parts.append(age_restrictions)
        
        # Clean and combine
        combined_text = ' '.join([str(part) for part in text_parts if part])
        return combined_text.lower()
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        
        return dot_product / (norm_vec1 * norm_vec2)
    
    def _get_importance_weight(self, importance: str) -> float:
        """Get numerical weight for importance level"""
        weights = {
            "high": 1.2,
            "medium": 1.0,
            "low": 0.8
        }
        return weights.get(importance, 1.0)
    
    def _select_best_tags(self, tag_scores: List[Tuple[str, float, float]]) -> List[str]:
        """Select best tags based on scores and thresholds"""
        
        # Sort by weighted score
        tag_scores.sort(key=lambda x: x[1], reverse=True)
        
        selected_tags = []
        
        # Apply different thresholds based on score ranking
        for i, (tag_name, weighted_score, raw_similarity) in enumerate(tag_scores):
            if i < 3 and raw_similarity > 0.6:  # Top 3 must have high similarity
                selected_tags.append(tag_name)
            elif i < 8 and raw_similarity > 0.4:  # Next 5 can have medium similarity
                selected_tags.append(tag_name)
            elif i < 15 and raw_similarity > 0.3:  # Lower threshold for remaining
                selected_tags.append(tag_name)
        
        # Limit total tags
        return selected_tags[:12]
    
    def _add_basic_tags(self, product_data: Dict[str, Any]) -> List[str]:
        """Add basic categorical tags that don't need ML"""
        
        basic_tags = []
        
        # Pet type
        pet_type = product_data.get('pet_type', '').lower()
        if pet_type:
            basic_tags.append(pet_type)
        
        # Category
        category = product_data.get('category', '').lower()
        if category:
            basic_tags.append(category)
        
        # Age groups (only specific ones)
        age_groups = product_data.get('age_group', [])
        for age in age_groups:
            if age.lower() not in ['all', 'any', 'all breed sizes']:
                basic_tags.append(age.lower())
        
        return basic_tags
    
    def _clean_tags(self, tags: List[str]) -> List[str]:
        """Clean and validate tags"""
        cleaned = []
        
        for tag in tags:
            if not tag or len(tag) < 2:
                continue
            
            # Clean the tag
            clean_tag = tag.strip().lower()
            clean_tag = re.sub(r'[^a-zA-Z0-9\-\s]', '', clean_tag)
            clean_tag = re.sub(r'\s+', '-', clean_tag)
            
            # Skip duplicates and very long tags
            if clean_tag not in cleaned and len(clean_tag) <= 20:
                cleaned.append(clean_tag)
        
        return cleaned[:15]  # Limit to 15 tags max
    
    def get_tag_explanations(self, product_data: Dict[str, Any], generated_tags: List[str]) -> Dict[str, float]:
        """Get similarity scores for generated tags to explain why they were chosen"""
        
        product_text = self._extract_product_text(product_data)
        product_embedding = self.model.encode(product_text)
        
        explanations = {}
        
        for tag in generated_tags:
            if tag in self.tag_database:
                similarity = self._cosine_similarity(
                    product_embedding, 
                    self.tag_database[tag]["embedding"]
                )
                explanations[tag] = round(similarity, 3)
            else:
                # Basic tags don't have explanations
                explanations[tag] = 1.0
        
        return explanations