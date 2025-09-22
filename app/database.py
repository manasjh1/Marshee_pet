import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Database:
    client = None
    database = None

    @classmethod
    def initialize(cls):
        """Initialize MongoDB  connection"""
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster = os.getenv("MONGODB_CLUSTER")
        database_name = os.getenv("DATABASE_NAME", "petRecommendationDB")
        
        if not all([username, password, cluster]):
            raise ValueError("Missing required MongoDB connection environment variables")
        
        # URL encode username and password
        username_encoded = quote_plus(username)
        password_encoded = quote_plus(password)
        
        # Build connection string with encoded credentials
        mongodb_url = f"mongodb+srv://{username_encoded}:{password_encoded}@{cluster}/{database_name}?retryWrites=true&w=majority&appName=Marshee"
        
        cls.client = MongoClient(mongodb_url)
        cls.database = cls.client[database_name]
        
        # Test connection
        try:
            cls.client.admin.command('ping')
            print(f"Successfully connected to MongoDB database: {database_name}")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a collection from the database"""
        if cls.database is None:
            cls.initialize()
        return cls.database[collection_name]

    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()

def get_products_collection():
    return Database.get_collection("products")

def get_pet_profiles_collection():
    return Database.get_collection("pet profile")  