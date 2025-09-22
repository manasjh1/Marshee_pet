from typing import List, Dict, Any, Set, Tuple
import re
from collections import Counter, defaultdict

class MLTagGenerator:
    """NLP-based keyword extraction tag generator"""
    
    def __init__(self):
        print("Loading NLP keyword-based tag generation system...")
        
        # Initialize keyword dictionaries
        self.health_keywords = self._initialize_health_keywords()
        self.nutrition_keywords = self._initialize_nutrition_keywords()
        self.quality_keywords = self._initialize_quality_keywords()
        self.functional_keywords = self._initialize_functional_keywords()
        self.ingredient_keywords = self._initialize_ingredient_keywords()
        self.stopwords = self._initialize_stopwords()
        
        print("NLP keyword extraction system loaded successfully!")
        print(f"Total keyword categories: {len(self.health_keywords) + len(self.nutrition_keywords) + len(self.quality_keywords)}")
    
    def _initialize_health_keywords(self) -> Dict[str, List[str]]:
        """Health-related keyword mappings"""
        return {
            "joint-support": [
                "joint", "joints", "arthritis", "hip", "dysplasia", "mobility", 
                "glucosamine", "chondroitin", "msm", "orthopedic", "cartilage"
            ],
            "digestive-health": [
                "digestive", "digestion", "stomach", "gut", "intestinal", "probiotic", 
                "prebiotic", "sensitive", "easy-digest", "fiber", "digestible"
            ],
            "skin-coat-health": [
                "skin", "coat", "fur", "dermatitis", "itchy", "shiny", "glossy", 
                "omega", "fatty-acids", "dull", "dry-skin"
            ],
            "dental-care": [
                "dental", "teeth", "tooth", "oral", "tartar", "plaque", "breath", 
                "gums", "chew", "cleaning"
            ],
            "heart-health": [
                "heart", "cardiac", "cardiovascular", "taurine", "circulation", 
                "blood-pressure", "cardio"
            ],
            "kidney-support": [
                "kidney", "renal", "urinary", "bladder", "phosphorus", "uti", 
                "urination", "nephritis"
            ],
            "immune-support": [
                "immune", "immunity", "antioxidant", "antioxidants", "vitamin-c", 
                "vitamin-e", "defense", "resistance"
            ],
            "weight-management": [
                "weight", "diet", "light", "lean", "calorie", "calories", "fat", 
                "obesity", "overweight", "slim", "reduction"
            ],
            "senior-care": [
                "senior", "elderly", "aged", "mature", "cognitive", "brain", 
                "memory", "aging", "old"
            ],
            "anxiety-relief": [
                "anxiety", "stress", "calm", "calming", "nervous", "relaxing", 
                "soothing", "comfort", "fearful"
            ],
            "allergy-relief": [
                "allergy", "allergies", "allergic", "hypoallergenic", "sensitive", 
                "reaction", "intolerance"
            ]
        }
    
    def _initialize_nutrition_keywords(self) -> Dict[str, List[str]]:
        """Nutrition-related keyword mappings"""
        return {
            "high-protein": [
                "high-protein", "protein-rich", "meat-first", "real-meat", 
                "protein", "muscle", "lean-muscle"
            ],
            "grain-free": [
                "grain-free", "gluten-free", "wheat-free", "corn-free", 
                "no-grain", "no-gluten", "grain-less"
            ],
            "plant-based": [
                "plant-based", "vegan", "vegetarian", "plant-protein", 
                "meat-free", "plant-derived", "botanical"
            ],
            "organic": [
                "organic", "usda-organic", "certified-organic", "naturally-grown", 
                "pesticide-free", "chemical-free"
            ],
            "natural": [
                "natural", "all-natural", "100%-natural", "wholesome", "pure", 
                "clean", "minimally-processed"
            ],
            "raw": [
                "raw", "freeze-dried", "dehydrated", "air-dried", "minimally-cooked", 
                "uncooked", "fresh"
            ],
            "limited-ingredient": [
                "limited-ingredient", "simple", "few-ingredients", "minimal", 
                "single-protein", "novel-protein"
            ],
            "superfood": [
                "superfood", "superfoods", "antioxidant-rich", "nutrient-dense", 
                "blueberry", "cranberry", "chia", "quinoa"
            ],
            "multivitamin": [
                "multivitamin", "multi-vitamin", "vitamin", "vitamins", "mineral", 
                "minerals", "supplement", "enriched"
            ],
            "omega-fatty-acids": [
                "omega-3", "omega-6", "fatty-acids", "fish-oil", "epa", "dha", 
                "flaxseed", "salmon-oil"
            ]
        }
    
    def _initialize_quality_keywords(self) -> Dict[str, List[str]]:
        """Quality and certification keyword mappings"""
        return {
            "vet-recommended": [
                "vet-recommended", "veterinarian", "veterinary", "vet-approved", 
                "doctor-recommended", "clinical"
            ],
            "human-grade": [
                "human-grade", "food-grade", "restaurant-quality", "kitchen-grade", 
                "human-quality"
            ],
            "premium": [
                "premium", "super-premium", "high-quality", "superior", "gourmet", 
                "luxury", "elite"
            ],
            "therapeutic": [
                "therapeutic", "prescription", "medical", "clinical", "treatment", 
                "therapy", "medicinal"
            ],
            "made-in-usa": [
                "made-in-usa", "usa-made", "american-made", "manufactured-usa", 
                "proudly-american"
            ],
            "no-artificial": [
                "no-artificial", "no-preservatives", "no-additives", "no-fillers", 
                "artificial-free", "preservative-free"
            ],
            "tested": [
                "tested", "quality-tested", "lab-tested", "safety-tested", 
                "third-party-tested", "verified"
            ]
        }
    
    def _initialize_functional_keywords(self) -> Dict[str, List[str]]:
        """Functional benefit keyword mappings"""
        return {
            "training": [
                "training", "reward", "treats", "motivation", "positive-reinforcement", 
                "obedience", "behavioral"
            ],
            "interactive": [
                "interactive", "puzzle", "mental-stimulation", "brain-game", 
                "challenging", "enrichment", "smart"
            ],
            "durable": [
                "durable", "tough", "strong", "heavy-duty", "long-lasting", 
                "indestructible", "chew-resistant"
            ],
            "comfort": [
                "comfort", "cozy", "soft", "plush", "cushioned", "padded", 
                "comfortable", "supportive"
            ],
            "waterproof": [
                "waterproof", "water-resistant", "washable", "easy-clean", 
                "machine-washable", "stain-resistant"
            ],
            "cooling": [
                "cooling", "cool", "temperature-regulation", "gel", "breathable", 
                "ventilated", "summer"
            ],
            "heating": [
                "heated", "warming", "warm", "thermal", "heat", "winter", "cold"
            ],
            "portable": [
                "portable", "travel", "lightweight", "compact", "foldable", 
                "on-the-go", "mobile"
            ]
        }
    
    def _initialize_ingredient_keywords(self) -> Dict[str, List[str]]:
        """Specific ingredient keyword mappings"""
        return {
            "chicken": ["chicken", "poultry", "fowl"],
            "beef": ["beef", "bovine", "cow"],
            "lamb": ["lamb", "sheep", "mutton"],
            "fish": ["fish", "salmon", "tuna", "cod", "whitefish", "seafood"],
            "duck": ["duck"],
            "turkey": ["turkey"],
            "venison": ["venison", "deer"],
            "pork": ["pork", "pig", "swine"],
            "sweet-potato": ["sweet-potato", "sweet-potatoes", "yam"],
            "rice": ["rice", "brown-rice", "white-rice"],
            "potato": ["potato", "potatoes"],
            "peas": ["pea", "peas", "green-peas"],
            "carrots": ["carrot", "carrots"],
            "pumpkin": ["pumpkin"],
            "blueberries": ["blueberry", "blueberries"],
            "cranberries": ["cranberry", "cranberries"],
            "spinach": ["spinach"],
            "kale": ["kale"],
            "oats": ["oat", "oats", "oatmeal"],
            "barley": ["barley"],
            "quinoa": ["quinoa"],
            "chia-seeds": ["chia", "chia-seeds"],
            "flaxseed": ["flax", "flaxseed", "linseed"]
        }
    
    def _initialize_stopwords(self) -> Set[str]:
        """Words to ignore during extraction"""
        return {
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", 
            "by", "from", "about", "into", "through", "during", "before", "after", 
            "above", "below", "up", "down", "out", "off", "over", "under", "again", 
            "further", "then", "once", "here", "there", "when", "where", "why", 
            "how", "all", "any", "both", "each", "few", "more", "most", "other", 
            "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
            "than", "too", "very", "can", "will", "just", "should", "now", "pet", 
            "pets", "animal", "animals", "product", "products", "item", "items"
        }
    
    def generate_tags(self, product_data: Dict[str, Any]) -> List[str]:
        """Generate tags using NLP keyword extraction"""
        
        # Extract all text content
        all_text = self._extract_all_text(product_data)
        
        if not all_text.strip():
            return self._get_basic_tags_fallback(product_data)
        
        # Clean and normalize text
        cleaned_text = self._clean_text(all_text)
        
        # Extract tags using different methods
        extracted_tags = set()
        
        # 1. Health keyword extraction
        health_tags = self._extract_keyword_tags(cleaned_text, self.health_keywords)
        extracted_tags.update(health_tags)
        
        # 2. Nutrition keyword extraction
        nutrition_tags = self._extract_keyword_tags(cleaned_text, self.nutrition_keywords)
        extracted_tags.update(nutrition_tags)
        
        # 3. Quality keyword extraction
        quality_tags = self._extract_keyword_tags(cleaned_text, self.quality_keywords)
        extracted_tags.update(quality_tags)
        
        # 4. Functional keyword extraction
        functional_tags = self._extract_keyword_tags(cleaned_text, self.functional_keywords)
        extracted_tags.update(functional_tags)
        
        # 5. Ingredient analysis
        ingredient_tags = self._extract_ingredient_tags(product_data)
        extracted_tags.update(ingredient_tags)
        
        # 6. Pattern-based extraction
        pattern_tags = self._extract_pattern_tags(cleaned_text)
        extracted_tags.update(pattern_tags)
        
        # 7. Numeric and percentage extraction
        numeric_tags = self._extract_numeric_tags(cleaned_text)
        extracted_tags.update(numeric_tags)
        
        # 8. Essential product info
        essential_tags = self._extract_essential_tags(product_data)
        extracted_tags.update(essential_tags)
        
        # Clean and finalize tags
        final_tags = self._finalize_tags(list(extracted_tags))
        
        print(f"Extracted {len(final_tags)} keyword-based tags")
        return final_tags
    
    def _extract_all_text(self, product_data: Dict[str, Any]) -> str:
        """Extract all text from product data"""
        
        text_parts = []
        
        # Primary text sources
        text_parts.append(product_data.get('name', ''))
        text_parts.append(product_data.get('description', ''))
        text_parts.append(product_data.get('Product_type', ''))
        text_parts.append(product_data.get('sub_category', ''))
        
        # Join lists
        text_parts.extend(product_data.get('age_group', []))
        text_parts.extend(product_data.get('breed_size', []))
        text_parts.extend(product_data.get('ingredients', []))
        
        # Safety and business data
        safety_data = product_data.get('safety', {})
        if isinstance(safety_data, dict):
            text_parts.extend(safety_data.get('allergens', []))
            text_parts.append(safety_data.get('age_restrictions', ''))
        
        return ' '.join(str(part) for part in text_parts if part)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for processing"""
        
        # Convert to lowercase
        text = text.lower()
        
        # Replace common separators with spaces
        text = re.sub(r'[,;:|/\\()[\]{}]', ' ', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra whitespace
        text = text.strip()
        
        return text
    
    def _extract_keyword_tags(self, text: str, keyword_dict: Dict[str, List[str]]) -> Set[str]:
        """Extract tags based on keyword dictionaries"""
        
        found_tags = set()
        
        for tag_name, keywords in keyword_dict.items():
            for keyword in keywords:
                # Create regex pattern for whole word matching
                pattern = r'\b' + re.escape(keyword.replace('-', '[ -]?')) + r'\b'
                
                if re.search(pattern, text):
                    found_tags.add(tag_name)
                    break  # Found one keyword for this tag, move to next tag
        
        return found_tags
    
    def _extract_ingredient_tags(self, product_data: Dict[str, Any]) -> Set[str]:
        """Extract tags based on ingredients"""
        
        ingredients = product_data.get('ingredients', [])
        if not ingredients:
            return set()
        
        ingredient_text = ' '.join(ingredients).lower()
        found_tags = set()
        
        for tag_name, keywords in self.ingredient_keywords.items():
            for keyword in keywords:
                if keyword.lower() in ingredient_text:
                    found_tags.add(tag_name)
                    break
        
        return found_tags
    
    def _extract_pattern_tags(self, text: str) -> Set[str]:
        """Extract tags using pattern matching - only meaningful ones"""
        
        pattern_tags = set()
        
        # Quality patterns (meaningful)
        if re.search(r'\b(non\s*gmo|no\s*gmo)\b', text):
            pattern_tags.add('non-gmo')
        
        if re.search(r'\bno\s+(artificial|preservatives|additives|fillers)\b', text):
            pattern_tags.add('no-artificial')
        
        # Specific formulations (meaningful)
        if re.search(r'\b(limited\s+ingredient|single\s+protein)\b', text):
            pattern_tags.add('limited-ingredient')
        
        # Processing methods (meaningful)
        if re.search(r'\b(freeze\s*dried|air\s*dried)\b', text):
            pattern_tags.add('freeze-dried')
        
        return pattern_tags
    
    def _extract_numeric_tags(self, text: str) -> Set[str]:
        """Extract tags from numeric information"""
        
        numeric_tags = set()
        
        # Protein content
        protein_match = re.search(r'(\d+)%?\s*protein', text)
        if protein_match:
            protein_val = int(protein_match.group(1))
            if protein_val >= 30:
                numeric_tags.add('high-protein')
            elif protein_val >= 18:
                numeric_tags.add('moderate-protein')
        
        # Fat content
        fat_match = re.search(r'(\d+)%?\s*fat', text)
        if fat_match:
            fat_val = int(fat_match.group(1))
            if fat_val <= 8:
                numeric_tags.add('low-fat')
            elif fat_val >= 15:
                numeric_tags.add('high-fat')
        
        # Calorie content
        calorie_match = re.search(r'(\d+)\s*cal', text)
        if calorie_match:
            cal_val = int(calorie_match.group(1))
            if cal_val <= 300:
                numeric_tags.add('low-calorie')
        
        return numeric_tags
    
    def _extract_essential_tags(self, product_data: Dict[str, Any]) -> Set[str]:
        """Extract essential product information tags - only specific/useful ones"""
        
        essential_tags = set()
        
        # Pet type
        pet_type = product_data.get('pet_type', '').lower().strip()
        if pet_type:
            essential_tags.add(pet_type)
        
        # Category
        category = product_data.get('category', '').lower().strip()
        if category:
            essential_tags.add(category)
        
        # Age groups (only specific ones)
        for age in product_data.get('age_group', []):
            age_clean = age.lower().strip()
            if age_clean in ['puppy', 'kitten', 'senior', 'adult']:
                essential_tags.add(age_clean)
        
        # Breed sizes - only if specifically mentioned, not "all sizes"
        breed_sizes = product_data.get('breed_size', [])
        specific_sizes = []
        
        for size in breed_sizes:
            size_clean = size.lower().strip()
            # Skip generic "all" sizes
            if 'all' in size_clean or 'any' in size_clean or 'universal' in size_clean:
                continue
            
            if 'small' in size_clean:
                specific_sizes.append('small-breed')
            elif 'large' in size_clean:
                specific_sizes.append('large-breed')
            elif 'medium' in size_clean:
                specific_sizes.append('medium-breed')
            elif 'giant' in size_clean:
                specific_sizes.append('giant-breed')
            elif 'toy' in size_clean:
                specific_sizes.append('toy-breed')
        
        # Only add breed size tags if there are 3 or fewer specific sizes
        # (avoid products that say "suitable for all sizes")
        if len(specific_sizes) <= 3:
            essential_tags.update(specific_sizes)
        
        return essential_tags
    
    def _finalize_tags(self, tags: List[str]) -> List[str]:
        """Clean and finalize the tag list - remove generic/marketing tags"""
        
        # Define tags to exclude (generic/marketing/useless)
        excluded_tags = {
            '100-percent', 'all-breed-sizes', 'all-life-stages', 'all-ages',
            'any-size', 'universal', 'complete', 'balanced', 'everyday',
            'regular', 'standard', 'normal', 'basic', 'general', 'common',
            'typical', 'usual', 'ordinary', 'simple', 'plain', 'traditional'
        }
        
        # Remove duplicates and clean
        cleaned_tags = []
        seen_tags = set()
        
        for tag in tags:
            if not tag:
                continue
                
            # Clean tag
            clean_tag = tag.strip().lower()
            clean_tag = re.sub(r'[^a-zA-Z0-9\-]', '', clean_tag)
            
            # Skip if empty, too short, or already seen
            if len(clean_tag) < 2 or clean_tag in seen_tags:
                continue
            
            # Skip if it's a stopword or excluded tag
            if clean_tag in self.stopwords or clean_tag in excluded_tags:
                continue
            
            # Skip overly generic ingredient tags for products with many ingredients
            if clean_tag in ['potato', 'peas', 'carrots'] and len(tags) > 10:
                continue
            
            cleaned_tags.append(clean_tag)
            seen_tags.add(clean_tag)
        
        # Sort by importance: health/nutrition first, then specifics
        priority_prefixes = [
            'joint', 'digestive', 'skin', 'dental', 'heart', 'kidney', 'weight', 
            'senior', 'anxiety', 'allergy', 'high-protein', 'grain-free', 
            'plant-based', 'organic', 'natural', 'vet', 'therapeutic'
        ]
        
        priority_tags = []
        other_tags = []
        
        for tag in cleaned_tags:
            is_priority = any(tag.startswith(prefix) for prefix in priority_prefixes)
            if is_priority:
                priority_tags.append(tag)
            else:
                other_tags.append(tag)
        
        # Combine priority tags first, then others
        final_tags = priority_tags + other_tags
        
        # Return up to 20 meaningful tags
        return final_tags[:20]
    
    def _get_basic_tags_fallback(self, product_data: Dict[str, Any]) -> List[str]:
        """Basic fallback when no text is available"""
        
        basic_tags = []
        
        if product_data.get('pet_type'):
            basic_tags.append(product_data['pet_type'].lower())
        
        if product_data.get('category'):
            basic_tags.append(product_data['category'].lower())
        
        return basic_tags
    
    def get_tag_explanations(self, product_data: Dict[str, Any], generated_tags: List[str]) -> Dict[str, float]:
        """Get explanations for why tags were generated"""
        
        explanations = {}
        all_text = self._extract_all_text(product_data).lower()
        
        for tag in generated_tags:
            # Check which keyword dictionary this tag might come from
            confidence = 0.8  # Default confidence for keyword matches
            
            # Check if it's an essential tag
            if tag in [product_data.get('pet_type', '').lower(), 
                      product_data.get('category', '').lower()]:
                confidence = 1.0
            
            # Check if it matches age group
            elif tag in [age.lower() for age in product_data.get('age_group', [])]:
                confidence = 1.0
            
            # Check if it's found in text directly
            elif tag.replace('-', ' ') in all_text or tag.replace('-', '') in all_text:
                confidence = 0.9
            
            explanations[tag] = confidence
        
        return explanations