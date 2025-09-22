#!/usr/bin/env python3
"""
Test script for the PAWS FOR GREENS wet dog food product
"""

import sys
import os
sys.path.append('.')

def test_paws_for_greens_product():
    """Test tag generation for the specific PAWS FOR GREENS product"""
    
    try:
        from app.services.ml_tag_generator import MLTagGenerator
        
        # Initialize the tag generator
        tag_gen = MLTagGenerator()
        
        # Create the exact product data from your description
        test_product = {
            "product_id": "PFGWDF02",
            "sku": "PFGWDF02",
            "brand": "PAWS FOR GREENS",
            "name": "PAWS FOR GREENS Wet Dog Food Real Veggies Ready to Eat Pet Food Human-Grade Ingredients, 100% Natural & Preservative-Free Veg Dog Food for Puppies & Adults (Pack of 2, Peas)",
            "pet_type": "Dog",
            "category": "Food",
            "sub_category": "Wet Food",
            "Product_type": "Vegan",
            "age_group": ["All Life Stages"],
            "breed_size": ["All Breed Sizes"],
            "ingredients": [
                "Peas", "Sweet Potatoes", "Chickpeas", "Brown Rice", "Lentils", 
                "Carrots", "Spinach", "Flaxseed", "Sunflower Oil"
            ],
            "description": """Give your furry friend a bowl full of love and nutrition with Paws for Greens Veggie Mix – the ultimate healthy veg gravy dog food designed for Indian dogs. This delicious plant-based wet dog food is made with 100% vegan ingredients and comes in a tasty gravy-style texture that dogs love. Ideal for sensitive stomachs and the Indian climate, our gravy dog food offers hydration, cooling, and easy digestion. Packed with moisture-rich, gut-friendly ingredients, this cruelty-free wet dog food helps keep your pet happy and healthy without any preservatives or artificial additives. Whether you're switching to a more sustainable pet diet or caring for a pup with dietary needs, our healthy veg gravy dog food is a smart, wholesome choice.
            
            Pure Plant Power: This wet gravy dog food blends chickpeas, pumpkin, and sweet potato—rich in fiber, potassium, and vitamins—for a healthy veg dog food boost.
            High Moisture Content: Keeps your pet hydrated with wet dog food rich in natural moisture—ideal for gravy dog food lovers and summer relief.
            No Preservatives, No BS: Clean and natural wet gravy dog food made for daily feeding—safe, healthy, and plant-powered.
            Easy to Digest: Made with brown rice and peas, this healthy veg dog food offers gentle nutrition in a tasty vegan wet dog food gravy.
            Made in India, With Love: Locally crafted vegan gravy dog food—proudly made for Indian pets with care and quality.""",
            
            "variants": [
                {
                    "variant_id": "PFGWDF02-PEAS",
                    "flavour": "Peas",
                    "weight_g": 200,
                    "price": {"currency": "INR", "mrp": 598, "selling_price": 559},
                    "stock_quantity": 50,
                    "is_available": True
                }
            ],
            
            "safety": {
                "allergens": ["BPA-Free"],
                "age_restrictions": "All Life Stages",
                "weight_restrictions": "",
                "health_warnings": []
            },
            
            "nutrition": {
                "protein_content": "High Protein",
                "diet_type": "Plant-Based, Vegan",
                "ingredient_claims": "Human-Grade, Organic",
                "nutrient_claims": "High Protein, No Added Sugar"
            },
            
            "business_data": {
                "popularity_score": 85,
                "avg_rating": 4.2,
                "total_reviews": 156,
                "margin_percent": 12,
                "is_premium": True
            },
            
            "metadata": {
                "country_origin": "India",
                "manufacturer": "DILO Pets Pvt. Ltd.",
                "specific_uses": ["Food", "Liver Care", "Training"],
                "item_form": "Granule"
            }
        }
        
        print("🧪 TESTING PAWS FOR GREENS WET DOG FOOD")
        print("=" * 60)
        print(f"Product: {test_product['name'][:80]}...")
        print(f"Brand: {test_product['brand']}")
        print(f"Category: {test_product['category']} - {test_product['sub_category']}")
        print(f"Ingredients: {', '.join(test_product['ingredients'][:5])}...")
        print()
        
        # Generate tags
        print("🏷️  GENERATING TAGS...")
        generated_tags = tag_gen.generate_tags(test_product)
        
        print(f"✅ Generated {len(generated_tags)} tags:")
        print(f"Tags: {generated_tags}")
        print()
        
        # Get explanations
        print("📊 TAG EXPLANATIONS:")
        explanations = tag_gen.get_tag_explanations(test_product, generated_tags)
        
        # Group tags by confidence level
        high_confidence = []
        medium_confidence = []
        low_confidence = []
        
        for tag, confidence in explanations.items():
            if confidence >= 0.9:
                high_confidence.append((tag, confidence))
            elif confidence >= 0.7:
                medium_confidence.append((tag, confidence))
            else:
                low_confidence.append((tag, confidence))
        
        print(f"🎯 HIGH CONFIDENCE (≥0.9): {len(high_confidence)} tags")
        for tag, conf in high_confidence:
            print(f"   • {tag}: {conf}")
        
        print(f"🎯 MEDIUM CONFIDENCE (0.7-0.9): {len(medium_confidence)} tags")
        for tag, conf in medium_confidence:
            print(f"   • {tag}: {conf}")
        
        print(f"🎯 LOW CONFIDENCE (<0.7): {len(low_confidence)} tags")
        for tag, conf in low_confidence:
            print(f"   • {tag}: {conf}")
        
        print()
        print("🏆 ANALYSIS:")
        print("=" * 60)
        
        # Analyze tag categories
        health_tags = [tag for tag in generated_tags if any(keyword in tag for keyword in 
                      ['joint', 'digestive', 'skin', 'dental', 'heart', 'kidney', 'liver', 'sensitive'])]
        
        nutrition_tags = [tag for tag in generated_tags if any(keyword in tag for keyword in 
                         ['protein', 'plant', 'vegan', 'organic', 'natural', 'grain'])]
        
        quality_tags = [tag for tag in generated_tags if any(keyword in tag for keyword in 
                       ['human-grade', 'premium', 'vet', 'therapeutic', 'no-artificial'])]
        
        ingredient_tags = [tag for tag in generated_tags if tag in 
                          ['peas', 'sweet-potato', 'chickpeas', 'rice', 'lentils', 'carrots', 'spinach']]
        
        functional_tags = [tag for tag in generated_tags if any(keyword in tag for keyword in 
                          ['training', 'digestible', 'hydrating', 'cooling', 'wet'])]
        
        print(f"🏥 Health & Wellness Tags: {health_tags}")
        print(f"🥗 Nutrition Tags: {nutrition_tags}")
        print(f"⭐ Quality Tags: {quality_tags}")
        print(f"🌱 Ingredient Tags: {ingredient_tags}")
        print(f"⚙️  Functional Tags: {functional_tags}")
        
        essential_tags = [tag for tag in generated_tags if tag in ['dog', 'food', 'puppy', 'adult']]
        print(f"📋 Essential Tags: {essential_tags}")
        
        print()
        print("💡 RECOMMENDATION INSIGHTS:")
        print("=" * 60)
        
        if 'plant-based' in generated_tags:
            print("✅ Perfect for vegetarian/vegan pet owners")
        
        if 'digestive-health' in generated_tags or 'sensitive' in any(generated_tags):
            print("✅ Good for pets with sensitive stomachs")
        
        if 'human-grade' in generated_tags:
            print("✅ High quality ingredients")
        
        if 'high-protein' in generated_tags:
            print("✅ Supports muscle development")
        
        if 'wet' in generated_tags or any('moisture' in tag for tag in generated_tags):
            print("✅ Helps with hydration")
        
        if 'training' in generated_tags:
            print("✅ Can be used for training rewards")
        
        print(f"\n🎯 FINAL RESULT: {len(generated_tags)} relevant, actionable tags generated!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_paws_for_greens_product()