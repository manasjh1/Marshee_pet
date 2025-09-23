from typing import List, Dict, Any, Set, Tuple
import re
from collections import Counter, defaultdict

class MLTagGenerator:
    """Enhanced NLP-based keyword extraction tag generator"""
    
    def __init__(self):
        print("Loading enhanced NLP keyword-based tag generation system...")
        
        # Initialize comprehensive keyword dictionaries
        self.health_keywords = self._initialize_health_keywords()
        self.nutrition_keywords = self._initialize_nutrition_keywords()
        self.quality_keywords = self._initialize_quality_keywords()
        self.functional_keywords = self._initialize_functional_keywords()
        self.ingredient_keywords = self._initialize_ingredient_keywords()
        self.texture_form_keywords = self._initialize_texture_form_keywords()
        self.age_specific_keywords = self._initialize_age_specific_keywords()
        self.condition_keywords = self._initialize_condition_keywords()
        self.stopwords = self._initialize_stopwords()
        
        print("Enhanced NLP keyword extraction system loaded successfully!")
        print(f"Total keyword categories: {len(self.health_keywords) + len(self.nutrition_keywords) + len(self.quality_keywords) + len(self.functional_keywords)}")
    
    def _initialize_health_keywords(self) -> Dict[str, List[str]]:
        """Comprehensive health-related keyword mappings"""
        return {
            "joint-support": [
                "joint", "joints", "arthritis", "hip", "dysplasia", "mobility", 
                "glucosamine", "chondroitin", "msm", "orthopedic", "cartilage",
                "stiffness", "inflammation", "bone-health"
            ],
            "digestive-health": [
                "digestive", "digestion", "stomach", "gut", "intestinal", "probiotic", 
                "prebiotic", "sensitive", "easy-digest", "fiber", "digestible",
                "gut-friendly", "stomach-friendly", "intestinal-health", "gut-health"
            ],
            "skin-coat-health": [
                "skin", "coat", "fur", "dermatitis", "itchy", "shiny", "glossy", 
                "omega", "fatty-acids", "dull", "dry-skin", "coat-shine",
                "healthy-skin", "skin-support", "coat-care"
            ],
            "dental-care": [
                "dental", "teeth", "tooth", "oral", "tartar", "plaque", "breath", 
                "gums", "chew", "cleaning", "oral-health", "dental-health",
                "teeth-cleaning", "fresh-breath"
            ],
            "heart-health": [
                "heart", "cardiac", "cardiovascular", "taurine", "circulation", 
                "blood-pressure", "cardio", "heart-support", "cardiovascular-health"
            ],
            "kidney-support": [
                "kidney", "renal", "urinary", "bladder", "phosphorus", "uti", 
                "urination", "nephritis", "kidney-health", "renal-support",
                "urinary-health", "bladder-health"
            ],
            "liver-support": [
                "liver", "hepatic", "liver-health", "liver-care", "liver-support",
                "detox", "detoxification", "hepatic-support"
            ],
            "immune-support": [
                "immune", "immunity", "antioxidant", "antioxidants", "vitamin-c", 
                "vitamin-e", "defense", "resistance", "immune-system",
                "immune-boost", "immune-health"
            ],
            "weight-management": [
                "weight", "diet", "light", "lean", "calorie", "calories", "fat", 
                "obesity", "overweight", "slim", "reduction", "weight-control",
                "weight-loss", "low-calorie", "diet-formula"
            ],
            "senior-care": [
                "senior", "elderly", "aged", "mature", "cognitive", "brain", 
                "memory", "aging", "old", "senior-support", "mature-care",
                "aging-support", "cognitive-support"
            ],
            "anxiety-relief": [
                "anxiety", "stress", "calm", "calming", "nervous", "relaxing", 
                "soothing", "comfort", "fearful", "stress-relief", "calming-support",
                "anti-anxiety", "relaxation"
            ],
            "allergy-relief": [
                "allergy", "allergies", "allergic", "hypoallergenic", "sensitive", 
                "reaction", "intolerance", "allergy-friendly", "sensitivity-support"
            ],
            "eye-health": [
                "eye", "eyes", "vision", "eye-health", "vision-support", 
                "lutein", "beta-carotene", "eye-care"
            ],
            "respiratory-health": [
                "respiratory", "breathing", "lungs", "airways", "respiratory-support",
                "lung-health", "breathing-support"
            ]
        }
    
    def _initialize_nutrition_keywords(self) -> Dict[str, List[str]]:
        """Enhanced nutrition-related keyword mappings"""
        return {
            "high-protein": [
                "high-protein", "protein-rich", "meat-first", "real-meat", 
                "protein", "muscle", "lean-muscle", "protein-packed"
            ],
            "grain-free": [
                "grain-free", "gluten-free", "wheat-free", "corn-free", 
                "no-grain", "no-gluten", "grain-less", "cereal-free"
            ],
            "plant-based": [
                "plant-based", "vegan", "vegetarian", "plant-protein", 
                "meat-free", "plant-derived", "botanical", "veggie",
                "plant-powered", "veg"
            ],
            "organic": [
                "organic", "usda-organic", "certified-organic", "naturally-grown", 
                "pesticide-free", "chemical-free", "bio-organic"
            ],
            "natural": [
                "natural", "all-natural", "100%-natural", "wholesome", "pure", 
                "clean", "minimally-processed", "nature-made"
            ],
            "raw": [
                "raw", "freeze-dried", "dehydrated", "air-dried", "minimally-cooked", 
                "uncooked", "fresh", "raw-diet", "fresh-frozen"
            ],
            "limited-ingredient": [
                "limited-ingredient", "simple", "few-ingredients", "minimal", 
                "single-protein", "novel-protein", "simple-recipe"
            ],
            "superfood": [
                "superfood", "superfoods", "antioxidant-rich", "nutrient-dense", 
                "blueberry", "cranberry", "chia", "quinoa", "nutrient-packed"
            ],
            "multivitamin": [
                "multivitamin", "multi-vitamin", "vitamin", "vitamins", "mineral", 
                "minerals", "supplement", "enriched", "fortified", "vitamin-enriched"
            ],
            "omega-fatty-acids": [
                "omega-3", "omega-6", "fatty-acids", "fish-oil", "epa", "dha", 
                "flaxseed", "salmon-oil", "healthy-fats"
            ],
            "low-fat": [
                "low-fat", "reduced-fat", "fat-free", "lean", "light-fat"
            ],
            "high-fiber": [
                "high-fiber", "fiber-rich", "dietary-fiber", "fiber", "fibrous"
            ],
            "gluten-free": [
                "gluten-free", "gluten-less", "no-gluten", "celiac-friendly"
            ],
            "preservative-free": [
                "preservative-free", "no-preservatives", "fresh-preserved",
                "naturally-preserved", "additive-free"
            ]
        }
    
    def _initialize_quality_keywords(self) -> Dict[str, List[str]]:
        """Enhanced quality and certification keyword mappings"""
        return {
            "vet-recommended": [
                "vet-recommended", "veterinarian", "veterinary", "vet-approved", 
                "doctor-recommended", "clinical", "vet-formulated"
            ],
            "human-grade": [
                "human-grade", "food-grade", "restaurant-quality", "kitchen-grade", 
                "human-quality", "human-consumption", "food-safety"
            ],
            "premium": [
                "premium", "super-premium", "high-quality", "superior", "gourmet", 
                "luxury", "elite", "top-quality", "finest"
            ],
            "therapeutic": [
                "therapeutic", "prescription", "medical", "clinical", "treatment", 
                "therapy", "medicinal", "health-focused"
            ],
            "made-in-usa": [
                "made-in-usa", "usa-made", "american-made", "manufactured-usa", 
                "proudly-american", "domestically-made"
            ],
            "no-artificial": [
                "no-artificial", "no-preservatives", "no-additives", "no-fillers", 
                "artificial-free", "preservative-free", "additive-free",
                "chemical-free", "no-chemicals"
            ],
            "tested": [
                "tested", "quality-tested", "lab-tested", "safety-tested", 
                "third-party-tested", "verified", "certified-safe"
            ],
            "non-gmo": [
                "non-gmo", "no-gmo", "gmo-free", "genetically-modified-free"
            ],
            "sustainably-sourced": [
                "sustainable", "sustainably-sourced", "eco-friendly", 
                "environmentally-friendly", "responsibly-sourced", "ethical"
            ]
        }
    
    def _initialize_functional_keywords(self) -> Dict[str, List[str]]:
        """Enhanced functional benefit keyword mappings"""
        return {
            "training": [
                "training", "reward", "treats", "motivation", "positive-reinforcement", 
                "obedience", "behavioral", "training-aid"
            ],
            "interactive": [
                "interactive", "puzzle", "mental-stimulation", "brain-game", 
                "challenging", "enrichment", "smart", "puzzle-toy"
            ],
            "durable": [
                "durable", "tough", "strong", "heavy-duty", "long-lasting", 
                "indestructible", "chew-resistant", "robust", "sturdy"
            ],
            "comfort": [
                "comfort", "cozy", "soft", "plush", "cushioned", "padded", 
                "comfortable", "supportive", "cozy-comfort"
            ],
            "waterproof": [
                "waterproof", "water-resistant", "washable", "easy-clean", 
                "machine-washable", "stain-resistant", "water-repellent"
            ],
            "cooling": [
                "cooling", "cool", "temperature-regulation", "gel", "breathable", 
                "ventilated", "summer", "heat-relief", "temperature-control"
            ],
            "heating": [
                "heated", "warming", "warm", "thermal", "heat", "winter", 
                "cold", "heated-comfort", "warmth"
            ],
            "portable": [
                "portable", "travel", "lightweight", "compact", "foldable", 
                "on-the-go", "mobile", "travel-friendly"
            ],
            "hydrating": [
                "hydrating", "moisture", "wet", "hydration", "moisture-rich",
                "high-moisture", "water-content"
            ],
            "easy-digest": [
                "easy-digest", "easily-digestible", "gentle", "mild", 
                "stomach-friendly", "digestible", "easy-on-stomach"
            ]
        }
    
    def _initialize_texture_form_keywords(self) -> Dict[str, List[str]]:
        """Food texture and form keywords"""
        return {
            "wet-food": [
                "wet", "moist", "gravy", "sauce", "pate", "chunks", 
                "wet-food", "canned", "pouch"
            ],
            "dry-food": [
                "dry", "kibble", "biscuits", "pellets", "dry-food", "crunchy"
            ],
            "soft-food": [
                "soft", "tender", "chewy", "semi-moist", "soft-bites"
            ],
            "treat-form": [
                "treats", "snacks", "bites", "chews", "strips", "sticks"
            ]
        }
    
    def _initialize_age_specific_keywords(self) -> Dict[str, List[str]]:
        """Age-specific formulation keywords"""
        return {
            "puppy-formula": [
                "puppy", "growth", "development", "young", "junior", 
                "puppy-formula", "growth-formula"
            ],
            "kitten-formula": [
                "kitten", "growth", "development", "young", "junior",
                "kitten-formula", "growth-formula"
            ],
            "adult-formula": [
                "adult", "maintenance", "adult-formula", "everyday"
            ],
            "senior-formula": [
                "senior", "mature", "aged", "elderly", "senior-formula",
                "mature-formula", "7+", "senior-care"
            ]
        }
    
    def _initialize_condition_keywords(self) -> Dict[str, List[str]]:
        """Specific health condition keywords"""
        return {
            "diabetes-friendly": [
                "diabetes", "diabetic", "blood-sugar", "glucose", "low-sugar"
            ],
            "kidney-disease": [
                "kidney-disease", "renal-disease", "ckd", "chronic-kidney"
            ],
            "heart-disease": [
                "heart-disease", "cardiac-disease", "heart-condition"
            ],
            "food-allergies": [
                "food-allergies", "food-sensitivities", "allergic-reactions"
            ],
            "obesity": [
                "obesity", "overweight", "weight-issues", "fat-reduction"
            ]
        }
    
    def _initialize_ingredient_keywords(self) -> Dict[str, List[str]]:
        """Enhanced specific ingredient keyword mappings"""
        return {
            "chicken": ["chicken", "poultry", "fowl", "chicken-meal"],
            "beef": ["beef", "bovine", "cow", "beef-meal"],
            "lamb": ["lamb", "sheep", "mutton", "lamb-meal"],
            "fish": ["fish", "salmon", "tuna", "cod", "whitefish", "seafood", "fish-meal"],
            "duck": ["duck", "duck-meal"],
            "turkey": ["turkey", "turkey-meal"],
            "venison": ["venison", "deer"],
            "pork": ["pork", "pig", "swine"],
            "sweet-potato": ["sweet-potato", "sweet-potatoes", "yam"],
            "rice": ["rice", "brown-rice", "white-rice"],
            "potato": ["potato", "potatoes"],
            "peas": ["pea", "peas", "green-peas"],
            "chickpeas": ["chickpea", "chickpeas", "garbanzo"],
            "lentils": ["lentil", "lentils"],
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
            "flaxseed": ["flax", "flaxseed", "linseed"],
            "sunflower-oil": ["sunflower-oil", "sunflower"],
            "coconut-oil": ["coconut-oil", "coconut"],
            "probiotics": ["probiotics", "lactobacillus", "bifidobacterium"],
            "prebiotics": ["prebiotics", "fos", "inulin"]
        }
    
    def _initialize_stopwords(self) -> Set[str]:
        """Enhanced words to ignore during extraction"""
        return {
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", 
            "by", "from", "about", "into", "through", "during", "before", "after", 
            "above", "below", "up", "down", "out", "off", "over", "under", "again", 
            "further", "then", "once", "here", "there", "when", "where", "why", 
            "how", "all", "any", "both", "each", "few", "more", "most", "other", 
            "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
            "than", "too", "very", "can", "will", "just", "should", "now", "pet", 
            "pets", "animal", "animals", "product", "products", "item", "items",
            "pack", "size", "brand", "flavour", "description", "information"
        }
    
    def generate_tags(self, product_data: Dict[str, Any]) -> List[str]:
        """Generate comprehensive tags using enhanced NLP keyword extraction"""
        
        # Extract all text content including additional fields
        all_text = self._extract_comprehensive_text(product_data)
        
        if not all_text.strip():
            return self._get_basic_tags_fallback(product_data)
        
        # Clean and normalize text
        cleaned_text = self._clean_text(all_text)
        
        # Extract tags using multiple enhanced methods
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
        
        # 5. Texture/form keyword extraction
        texture_tags = self._extract_keyword_tags(cleaned_text, self.texture_form_keywords)
        extracted_tags.update(texture_tags)
        
        # 6. Age-specific keyword extraction
        age_tags = self._extract_keyword_tags(cleaned_text, self.age_specific_keywords)
        extracted_tags.update(age_tags)
        
        # 7. Health condition keyword extraction
        condition_tags = self._extract_keyword_tags(cleaned_text, self.condition_keywords)
        extracted_tags.update(condition_tags)
        
        # 8. Enhanced ingredient analysis
        ingredient_tags = self._extract_enhanced_ingredient_tags(product_data, cleaned_text)
        extracted_tags.update(ingredient_tags)
        
        # 9. Enhanced pattern-based extraction
        pattern_tags = self._extract_enhanced_pattern_tags(cleaned_text)
        extracted_tags.update(pattern_tags)
        
        # 10. Numeric and percentage extraction
        numeric_tags = self._extract_numeric_tags(cleaned_text)
        extracted_tags.update(numeric_tags)
        
        # 11. Enhanced essential product info
        essential_tags = self._extract_enhanced_essential_tags(product_data)
        extracted_tags.update(essential_tags)
        
        # 12. Context-aware tags
        context_tags = self._extract_context_tags(product_data, cleaned_text)
        extracted_tags.update(context_tags)
        
        # Clean and finalize tags with better logic
        final_tags = self._finalize_enhanced_tags(list(extracted_tags), product_data)
        
        print(f"Extracted {len(final_tags)} enhanced keyword-based tags")
        return final_tags
    
    def _extract_comprehensive_text(self, product_data: Dict[str, Any]) -> str:
        """Extract all relevant text from product data including metadata"""
        
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
        
        # Nutrition data
        nutrition_data = product_data.get('nutrition', {})
        if isinstance(nutrition_data, dict):
            text_parts.append(nutrition_data.get('diet_type', ''))
            text_parts.append(nutrition_data.get('ingredient_claims', ''))
            text_parts.append(nutrition_data.get('nutrient_claims', ''))
        
        # Metadata
        metadata = product_data.get('metadata', {})
        if isinstance(metadata, dict):
            specific_uses = metadata.get('specific_uses', [])
            if isinstance(specific_uses, list):
                text_parts.extend(specific_uses)
            text_parts.append(metadata.get('item_form', ''))
        
        return ' '.join(str(part) for part in text_parts if part)
    
    def _extract_enhanced_ingredient_tags(self, product_data: Dict[str, Any], text: str) -> Set[str]:
        """Enhanced ingredient tag extraction with context"""
        
        ingredients = product_data.get('ingredients', [])
        if not ingredients:
            return set()
        
        ingredient_text = ' '.join(ingredients).lower()
        found_tags = set()
        
        # Primary ingredient tagging
        for tag_name, keywords in self.ingredient_keywords.items():
            for keyword in keywords:
                if keyword.lower() in ingredient_text:
                    found_tags.add(tag_name)
                    break
        
        # Add contextual ingredient tags
        if len(ingredients) <= 5:
            found_tags.add('limited-ingredient')
        
        # Check for protein combinations
        protein_sources = ['chicken', 'beef', 'lamb', 'fish', 'duck', 'turkey']
        protein_count = sum(1 for protein in protein_sources if protein in found_tags)
        
        if protein_count >= 2:
            found_tags.add('multi-protein')
        elif protein_count == 1:
            found_tags.add('single-protein')
        
        return found_tags
    
    def _extract_enhanced_pattern_tags(self, text: str) -> Set[str]:
        """Enhanced pattern matching with more comprehensive patterns"""
        
        pattern_tags = set()
        
        # Quality patterns
        if re.search(r'\b(non\s*gmo|no\s*gmo|gmo\s*free)\b', text):
            pattern_tags.add('non-gmo')
        
        if re.search(r'\bno\s+(artificial|preservatives|additives|fillers|chemicals)\b', text):
            pattern_tags.add('no-artificial')
        
        if re.search(r'\b(bpa\s*free|bpa-free)\b', text):
            pattern_tags.add('bpa-free')
        
        # Formulation patterns
        if re.search(r'\b(limited\s+ingredient|single\s+protein|novel\s+protein)\b', text):
            pattern_tags.add('limited-ingredient')
        
        # Processing patterns
        if re.search(r'\b(freeze\s*dried|air\s*dried|dehydrated)\b', text):
            pattern_tags.add('freeze-dried')
        
        if re.search(r'\b(slow\s*cooked|gently\s*cooked|low\s*temperature)\b', text):
            pattern_tags.add('slow-cooked')
        
        # Certification patterns
        if re.search(r'\b(usda\s*organic|certified\s*organic)\b', text):
            pattern_tags.add('certified-organic')
        
        # Special diet patterns
        if re.search(r'\b(raw\s*diet|barf\s*diet)\b', text):
            pattern_tags.add('raw-diet')
        
        return pattern_tags
    
    def _extract_enhanced_essential_tags(self, product_data: Dict[str, Any]) -> Set[str]:
        """Enhanced essential tag extraction - only truly distinctive tags"""
        
        essential_tags = set()
        
        # Pet type (keep this as it's discriminative between cats/dogs)
        pet_type = product_data.get('pet_type', '').lower().strip()
        if pet_type:
            essential_tags.add(pet_type)
        
        # Skip generic category - not helpful for recommendations
        # Instead, focus on sub-category if it's specific
        sub_category = product_data.get('sub_category', '').lower().strip()
        if sub_category and sub_category not in ['food', 'treats', 'toys', 'accessories']:
            essential_tags.add(sub_category.replace(' ', '-'))
        
        # Age groups (only specific ones)
        for age in product_data.get('age_group', []):
            age_clean = age.lower().strip()
            if age_clean in ['puppy', 'kitten', 'senior', 'adult', 'junior']:
                essential_tags.add(age_clean)
        
        # Breed sizes - only if specific (discriminative)
        breed_sizes = product_data.get('breed_size', [])
        if breed_sizes and not any('all' in size.lower() for size in breed_sizes):
            specific_sizes = set()
            for size in breed_sizes:
                size_clean = size.lower().strip()
                if 'small' in size_clean or 'toy' in size_clean:
                    specific_sizes.add('small-breed')
                elif 'large' in size_clean:
                    specific_sizes.add('large-breed')
                elif 'medium' in size_clean:
                    specific_sizes.add('medium-breed')
                elif 'giant' in size_clean:
                    specific_sizes.add('giant-breed')
            
            # Only add if there are 2 or fewer sizes (shows specificity)
            if len(specific_sizes) <= 2:
                essential_tags.update(specific_sizes)
        
        return essential_tags
    
    def _extract_context_tags(self, product_data: Dict[str, Any], text: str) -> Set[str]:
        """Extract context-aware tags based on product category and content"""
        
        context_tags = set()
        category = product_data.get('category', '').lower()
        
        # Food-specific context tags
        if 'food' in category:
            if 'complete' in text or 'balanced' in text:
                context_tags.add('complete-nutrition')
            if 'daily' in text or 'everyday' in text:
                context_tags.add('daily-feeding')
            if 'meal' in text:
                context_tags.add('main-meal')
        
        # Treat-specific context tags
        elif 'treat' in category:
            if 'training' in text or 'reward' in text:
                context_tags.add('training-treats')
            if 'healthy' in text:
                context_tags.add('healthy-treats')
        
        # Toy-specific context tags
        elif 'toy' in category:
            if 'mental' in text or 'brain' in text:
                context_tags.add('mental-enrichment')
            if 'exercise' in text or 'active' in text:
                context_tags.add('physical-exercise')
        
        # Size-based context
        if 'small' in text and 'breed' in text:
            context_tags.add('small-dog-friendly')
        elif 'large' in text and 'breed' in text:
            context_tags.add('large-dog-friendly')
        
        return context_tags
    
    def _finalize_enhanced_tags(self, tags: List[str], product_data: Dict[str, Any]) -> List[str]:
        """Enhanced tag finalization with smarter filtering and prioritization"""
        
        # Define enhanced exclusion list - remove generic category tags
        excluded_tags = {
            '100-percent', 'all-breed-sizes', 'all-life-stages', 'all-ages',
            'any-size', 'universal', 'complete', 'balanced', 'everyday',
            'regular', 'standard', 'normal', 'basic', 'general', 'common',
            'typical', 'usual', 'ordinary', 'simple', 'plain', 'traditional',
            'good', 'great', 'best', 'perfect', 'ideal', 'ultimate',
            # Remove generic category tags that don't add value
            'food', 'treats', 'toys', 'accessories', 'grooming', 'bed'
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
            
            # Smart ingredient filtering
            ingredient_count = len(product_data.get('ingredients', []))
            if clean_tag in ['potato', 'peas', 'carrots', 'rice'] and ingredient_count > 8:
                continue
            
            cleaned_tags.append(clean_tag)
            seen_tags.add(clean_tag)
        
        # Enhanced prioritization with multiple tiers
        tier1_prefixes = ['joint', 'digestive', 'skin', 'dental', 'heart', 'kidney', 'liver']
        tier2_prefixes = ['anxiety', 'allergy', 'weight', 'senior', 'immune']
        tier3_prefixes = ['high-protein', 'grain-free', 'plant-based', 'organic', 'natural']
        tier4_prefixes = ['vet', 'therapeutic', 'human-grade', 'premium']
        
        tier1_tags = []
        tier2_tags = []
        tier3_tags = []
        tier4_tags = []
        other_tags = []
        
        for tag in cleaned_tags:
            if any(tag.startswith(prefix) for prefix in tier1_prefixes):
                tier1_tags.append(tag)
            elif any(tag.startswith(prefix) for prefix in tier2_prefixes):
                tier2_tags.append(tag)
            elif any(tag.startswith(prefix) for prefix in tier3_prefixes):
                tier3_tags.append(tag)
            elif any(tag.startswith(prefix) for prefix in tier4_prefixes):
                tier4_tags.append(tag)
            else:
                other_tags.append(tag)
        
        # Combine all tiers in priority order
        final_tags = tier1_tags + tier2_tags + tier3_tags + tier4_tags + other_tags
        
        # Return up to 25 meaningful tags for better coverage
        return final_tags[:25]
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning and normalization"""
        
        # Convert to lowercase
        text = text.lower()
        
        # Replace common separators with spaces
        text = re.sub(r'[,;:|/\\()[\]{}]', ' ', text)
        
        # Replace hyphens in compound words with spaces for better matching
        text = re.sub(r'([a-z])-([a-z])', r'\1 \2', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove extra whitespace
        text = text.strip()
        
        return text
    
    def _extract_keyword_tags(self, text: str, keyword_dict: Dict[str, List[str]]) -> Set[str]:
        """Enhanced keyword tag extraction with fuzzy matching"""
        
        found_tags = set()
        
        for tag_name, keywords in keyword_dict.items():
            match_count = 0
            for keyword in keywords:
                # Create multiple patterns for flexible matching
                patterns = [
                    r'\b' + re.escape(keyword) + r'\b',  # Exact match
                    r'\b' + re.escape(keyword.replace('-', ' ')) + r'\b',  # Space instead of hyphen
                    r'\b' + re.escape(keyword.replace('-', '')) + r'\b'  # No separator
                ]
                
                for pattern in patterns:
                    if re.search(pattern, text):
                        match_count += 1
                        break
            
            # Add tag if any keywords match
            if match_count > 0:
                found_tags.add(tag_name)
        
        return found_tags
    
    def _extract_numeric_tags(self, text: str) -> Set[str]:
        """Enhanced numeric information extraction"""
        
        numeric_tags = set()
        
        # Protein content with more patterns
        protein_patterns = [
            r'(\d+)%?\s*protein',
            r'protein[:\s]*(\d+)%?',
            r'(\d+)%?\s*crude\s*protein'
        ]
        
        for pattern in protein_patterns:
            match = re.search(pattern, text)
            if match:
                protein_val = int(match.group(1))
                if protein_val >= 35:
                    numeric_tags.add('very-high-protein')
                elif protein_val >= 25:
                    numeric_tags.add('high-protein')
                elif protein_val >= 18:
                    numeric_tags.add('moderate-protein')
                break
        
        # Fat content
        fat_patterns = [
            r'(\d+)%?\s*fat',
            r'fat[:\s]*(\d+)%?',
            r'(\d+)%?\s*crude\s*fat'
        ]
        
        for pattern in fat_patterns:
            match = re.search(pattern, text)
            if match:
                fat_val = int(match.group(1))
                if fat_val <= 5:
                    numeric_tags.add('very-low-fat')
                elif fat_val <= 10:
                    numeric_tags.add('low-fat')
                elif fat_val >= 18:
                    numeric_tags.add('high-fat')
                break
        
        # Moisture content
        moisture_match = re.search(r'(\d+)%?\s*moisture', text)
        if moisture_match:
            moisture_val = int(moisture_match.group(1))
            if moisture_val >= 75:
                numeric_tags.add('high-moisture')
            elif moisture_val <= 12:
                numeric_tags.add('dry-food')
        
        # Fiber content
        fiber_match = re.search(r'(\d+)%?\s*(fiber|fibre)', text)
        if fiber_match:
            fiber_val = int(fiber_match.group(1))
            if fiber_val >= 8:
                numeric_tags.add('high-fiber')
            elif fiber_val <= 3:
                numeric_tags.add('low-fiber')
        
        return numeric_tags
    
    def _get_basic_tags_fallback(self, product_data: Dict[str, Any]) -> List[str]:
        """Enhanced basic fallback when no text is available"""
        
        basic_tags = []
        
        if product_data.get('pet_type'):
            basic_tags.append(product_data['pet_type'].lower())
        
        if product_data.get('category'):
            basic_tags.append(product_data['category'].lower())
        
        # Add sub-category if different from category
        sub_cat = product_data.get('sub_category', '')
        if sub_cat and sub_cat.lower() != product_data.get('category', '').lower():
            basic_tags.append(sub_cat.lower().replace(' ', '-'))
        
        return basic_tags
    
    def get_tag_explanations(self, product_data: Dict[str, Any], generated_tags: List[str]) -> Dict[str, float]:
        """Enhanced explanations for why tags were generated"""
        
        explanations = {}
        all_text = self._extract_comprehensive_text(product_data).lower()
        
        for tag in generated_tags:
            confidence = 0.8  # Default confidence
            
            # Essential tags get highest confidence
            if tag in [product_data.get('pet_type', '').lower(), 
                      product_data.get('category', '').lower()]:
                confidence = 1.0
            
            # Age group matches
            elif tag in [age.lower() for age in product_data.get('age_group', [])]:
                confidence = 1.0
            
            # Direct text matches
            elif tag.replace('-', ' ') in all_text:
                confidence = 0.95
            elif tag.replace('-', '') in all_text:
                confidence = 0.9
            
            # Ingredient-based tags
            elif tag in self.ingredient_keywords:
                ingredients_text = ' '.join(product_data.get('ingredients', [])).lower()
                for keyword in self.ingredient_keywords[tag]:
                    if keyword in ingredients_text:
                        confidence = 0.9
                        break
            
            # Health/nutrition tags get higher confidence if found in description
            elif any(tag.startswith(prefix) for prefix in ['joint', 'digestive', 'skin', 'dental']):
                if any(keyword in all_text for keyword in ['health', 'support', 'care', 'formula']):
                    confidence = 0.85
            
            explanations[tag] = confidence
        
        return explanations