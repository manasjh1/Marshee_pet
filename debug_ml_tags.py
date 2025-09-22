#!/usr/bin/env python3
"""
Debug script to test ML tag generation
"""

import sys
import os
sys.path.append('.')

def test_ml_tags():
    try:
        print("Testing ML tag generation...")
        
        # Test import
        from app.services.ml_tag_generator import MLTagGenerator
        print("✅ ML tag generator imported successfully")
        
        # Test initialization
        tag_gen = MLTagGenerator()
        print("✅ ML tag generator initialized successfully")
        
        # Test with your existing product
        test_product = {
            "product_id": "001",
            "name": "PAWS FOR GREENS Multivitamin Vegan Dog Food 100% Natural Plant-Based",
            "pet_type": "Dog",
            "category": "Food",
            "sub_category": "Dry Food",
            "Product_type": "Vegan",
            "age_group": ["Puppy"],
            "breed_size": ["All Breed Sizes", "Giant", "Large", "Medium"],
            "ingredients": ["pea protein", "potato protein", "sweet potato"],
            "description": "Supports complete health: Packed with essential nutrients from plant-based ingredients"
        }
        
        # Generate tags
        generated_tags = tag_gen.generate_tags(test_product)
        print(f"✅ Generated {len(generated_tags)} tags: {generated_tags}")
        
        # Get explanations
        explanations = tag_gen.get_tag_explanations(test_product, generated_tags)
        print("✅ Tag explanations:")
        for tag, score in explanations.items():
            print(f"   {tag}: {score}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Solution: Make sure sentence-transformers is installed: pip install sentence-transformers")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_ml_tags()