# test_db.py
from app.database import Database, get_pet_profiles_collection

Database.initialize()
pets_collection = get_pet_profiles_collection()

# Check what pets exist
all_pets = list(pets_collection.find({}))
print(f"Found {len(all_pets)} pets in database:")

for pet in all_pets:
    print(f"- Pet ID: {pet.get('pet_id')} | Name: {pet.get('name')} | Category: {pet.get('category')}")

# Check collection names
db = Database.database
collections = db.list_collection_names()
print(f"\nAvailable collections: {collections}")