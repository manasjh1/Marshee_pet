import sys
import os
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
print("Debug - Environment variables:")
print(f"USERNAME: {os.getenv('MONGODB_USERNAME')}")
print(f"CLUSTER: {os.getenv('MONGODB_CLUSTER')}")
print(f"DATABASE_NAME: {os.getenv('DATABASE_NAME')}")
print(f"PASSWORD: {os.getenv('MONGODB_PASSWORD')}")

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import Database, get_pet_profiles_collection, get_products_collection
from app.models.pet import PetProfile
from app.services.safety_filter import SafetyFilter

def test_database_connection():
    """Test if we can connect to MongoDB and fetch data"""
    print("Testing database connection...")
    
    try:
        # Initialize database
        Database.initialize()
        
        # Test pet profiles collection
        pets_collection = get_pet_profiles_collection()
        pet_count = pets_collection.count_documents({})
        print(f"✅ Found {pet_count} pet profiles")
        
        # Test products collection
        products_collection = get_products_collection()
        product_count = products_collection.count_documents({})
        print(f"✅ Found {product_count} products")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_safety_filter():
    """Test safety filtering with sample data"""
    print("\nTesting safety filter...")
    
    try:
        # Get collections
        pets_collection = get_pet_profiles_collection()
        products_collection = get_products_collection()
        
        # Fetch one pet and one product for testing
        pet_data = pets_collection.find_one({"pet_id": "PET001"})  # Buddy
        product_data = products_collection.find_one({"product_id": "001"})  # Vegan dog food
        
        if not pet_data or not product_data:
            print("❌ Could not find test pet or product")
            return False
            
        # Convert pet data to PetProfile model
        pet = PetProfile(**pet_data)
        
        # Test safety filter
        is_safe = SafetyFilter.is_product_safe_for_pet(pet, product_data)
        reasons = SafetyFilter.get_safety_reasons(pet, product_data)
        
        print(f"✅ Pet: {pet.name} ({pet.age_group} {pet.category})")
        print(f"✅ Product: {product_data.get('name', 'Unknown')}")
        print(f"✅ Is safe: {is_safe}")
        
        if not is_safe:
            print(f"❌ Safety concerns: {reasons}")
        else:
            print("✅ No safety concerns found")
            
        return True
        
    except Exception as e:
        print(f"❌ Safety filter test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Pet Recommendation System Tests\n")
    
    # Test database connection
    db_success = test_database_connection()
    
    if db_success:
        # Test safety filter
        filter_success = test_safety_filter()
        
        if filter_success:
            print("\n🎉 All tests passed! Your system is ready for development.")
        else:
            print("\n⚠️ Safety filter tests failed. Check your data models.")
    else:
        print("\n⚠️ Database connection failed. Check your .env file and MongoDB connection.")

if __name__ == "__main__":
    main()