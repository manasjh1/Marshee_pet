from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.database import get_products_collection
from bson import ObjectId
import traceback

router = APIRouter(prefix="/products", tags=["products"])

# Initialize ML tag generator (lazy loading)
ml_tag_generator = None

def get_ml_tag_generator():
    """Get ML tag generator instance with error handling"""
    global ml_tag_generator
    if ml_tag_generator is None:
        try:
            print("Loading ML tag generation model...")
            from app.services.ml_tag_generator import MLTagGenerator
            ml_tag_generator = MLTagGenerator()
            print("✅ ML model loaded successfully!")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Please install: pip install sentence-transformers")
            raise HTTPException(status_code=500, detail="ML libraries not installed. Run: pip install sentence-transformers")
        except Exception as e:
            print(f"❌ ML model loading error: {e}")
            print(f"Full traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"ML model loading failed: {str(e)}")
    return ml_tag_generator

class ProductCreate(BaseModel):
    """Model for creating a new product with all schema fields"""
    product_id: str
    sku: str
    brand: str
    name: str
    pet_type: str
    category: str
    sub_category: str = ""
    age_group: List[str] = Field(default_factory=list)
    breed_size: List[str] = Field(default_factory=list)
    ingredients: List[str] = Field(default_factory=list)
    description: str = ""
    
    # Variants matching your schema exactly
    variants: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Safety information matching your schema
    safety: Dict[str, Any] = Field(default_factory=dict)
    
    # Nutrition data matching your schema  
    nutrition: Dict[str, Any] = Field(default_factory=dict)
    
    # Business data matching your schema
    business_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Metadata matching your schema
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Optional fields matching your schema
    Product_type: str = "Regular"  # Capital P to match your schema
    status: str = "active"

@router.post("/")
def create_product_with_ml_tags(product_data: ProductCreate):
    """Create a new product with ML-generated tags"""
    products_collection = get_products_collection()
    
    # Check if product_id already exists
    existing_product = products_collection.find_one({"product_id": product_data.product_id})
    if existing_product:
        raise HTTPException(status_code=400, detail=f"Product with ID {product_data.product_id} already exists")
    
    try:
        # Convert to dict
        product_dict = product_data.dict()
        
        # Try to generate ML tags
        try:
            tag_gen = get_ml_tag_generator()
            generated_tags = tag_gen.generate_tags(product_dict)
            tag_explanations = tag_gen.get_tag_explanations(product_dict, generated_tags)
            
            # Add generated tags to product
            product_dict["tags"] = generated_tags
            
            ml_success = True
            ml_analysis = {
                "generated_tags": generated_tags,
                "tags_count": len(generated_tags),
                "tag_explanations": tag_explanations,
                "generation_method": "ML_embeddings"
            }
            
        except Exception as ml_error:
            print(f"❌ ML tag generation failed: {ml_error}")
            # Fallback: add basic tags manually
            basic_tags = []
            if product_dict.get('pet_type'):
                basic_tags.append(product_dict['pet_type'].lower())
            if product_dict.get('category'):
                basic_tags.append(product_dict['category'].lower())
            if product_dict.get('Product_type'):
                basic_tags.append(product_dict['Product_type'].lower())
            
            product_dict["tags"] = basic_tags
            ml_success = False
            ml_analysis = {
                "generated_tags": basic_tags,
                "tags_count": len(basic_tags),
                "generation_method": "basic_fallback",
                "ml_error": str(ml_error)
            }
        
        # Add timestamps
        product_dict["created_at"] = datetime.now().isoformat()
        product_dict["updated_at"] = datetime.now().isoformat()
        
        # Insert product
        result = products_collection.insert_one(product_dict)
        
        # Return created product
        created_product = products_collection.find_one({"_id": result.inserted_id})
        created_product["_id"] = str(created_product["_id"])
        
        return {
            "message": "Product created successfully" + (" with ML-generated tags" if ml_success else " with basic tags (ML failed)"),
            "product": created_product,
            "ml_analysis": ml_analysis,
            "ml_generation_success": ml_success
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.post("/preview-ml-tags")
def preview_ml_generated_tags(product_data: ProductCreate):
    """Preview what ML tags would be generated without saving the product"""
    
    try:
        product_dict = product_data.dict()
        
        # Generate tags using ML
        tag_gen = get_ml_tag_generator()
        generated_tags = tag_gen.generate_tags(product_dict)
        tag_explanations = tag_gen.get_tag_explanations(product_dict, generated_tags)
        
        # Categorize tags for better understanding
        tag_categories = {
            "health_medical": [tag for tag in generated_tags if any(keyword in tag for keyword in ['health', 'support', 'care', 'medical', 'joint', 'dental', 'heart', 'kidney'])],
            "dietary_nutrition": [tag for tag in generated_tags if any(keyword in tag for keyword in ['protein', 'grain', 'vegan', 'organic', 'natural', 'food'])],
            "life_stage": [tag for tag in generated_tags if any(keyword in tag for keyword in ['puppy', 'kitten', 'adult', 'senior', 'formula'])],
            "product_type": [tag for tag in generated_tags if any(keyword in tag for keyword in ['toy', 'bed', 'accessories', 'grooming'])],
            "quality_premium": [tag for tag in generated_tags if any(keyword in tag for keyword in ['premium', 'vet', 'therapeutic', 'orthopedic'])]
        }
        
        return {
            "product_name": product_data.name,
            "product_category": product_data.category,
            "ml_analysis": {
                "total_tags_generated": len(generated_tags),
                "generated_tags": generated_tags,
                "tag_explanations": tag_explanations,
                "tag_categories": tag_categories,
                "confidence_summary": {
                    "high_confidence": [tag for tag, score in tag_explanations.items() if score > 0.8],
                    "medium_confidence": [tag for tag, score in tag_explanations.items() if 0.6 <= score <= 0.8],
                    "low_confidence": [tag for tag, score in tag_explanations.items() if score < 0.6]
                }
            }
        }
        
    except Exception as e:
        # Return error details for debugging
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "ml_analysis": {
                "total_tags_generated": 0,
                "generated_tags": [],
                "error_message": "ML tag generation failed"
            }
        }

@router.get("/{product_id}")
def get_product(product_id: str):
    """Get a specific product by product_id"""
    products_collection = get_products_collection()
    
    product = products_collection.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
    
    # Convert ObjectId to string
    product["_id"] = str(product["_id"])
    
    return product

@router.get("/")
def list_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(50, ge=1, le=200, description="Number of products to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    pet_type: Optional[str] = Query(None, description="Filter by pet type"),
    brand: Optional[str] = Query(None, description="Filter by brand"),
    status: str = Query("active", description="Filter by status")
):
    """List products with filtering and pagination"""
    products_collection = get_products_collection()
    
    # Build query
    query = {"status": status}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if pet_type:
        query["pet_type"] = {"$regex": pet_type, "$options": "i"}
    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}
    
    # Get products
    products_cursor = products_collection.find(query).skip(skip).limit(limit)
    products = list(products_cursor)
    
    # Convert ObjectIds to strings and add tag info
    for product in products:
        product["_id"] = str(product["_id"])
        product["tag_count"] = len(product.get("tags", []))
    
    # Get total count
    total_count = products_collection.count_documents(query)
    
    return {
        "products": products,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total_count,
            "returned": len(products)
        },
        "filters_applied": {
            "category": category,
            "pet_type": pet_type,
            "brand": brand,
            "status": status
        }
    }

@router.get("/ml-stats")
def get_ml_tag_statistics():
    """Get ML tag generation statistics"""
    products_collection = get_products_collection()
    
    # Get products with tags
    products_with_tags = list(products_collection.find({"tags": {"$exists": True, "$ne": []}}))
    total_products = products_collection.count_documents({"status": "active"})
    
    if not products_with_tags:
        return {
            "message": "No products with ML-generated tags found",
            "ml_tag_statistics": {
                "total_products": total_products,
                "products_with_tags": 0,
                "ml_coverage_percentage": "0%"
            }
        }
    
    # Analyze tag distribution
    all_tags = []
    for product in products_with_tags:
        all_tags.extend(product.get("tags", []))
    
    from collections import Counter
    tag_frequency = Counter(all_tags)
    
    return {
        "ml_tag_statistics": {
            "total_products": total_products,
            "products_with_tags": len(products_with_tags),
            "ml_coverage_percentage": f"{(len(products_with_tags)/total_products*100):.1f}%" if total_products > 0 else "0%",
            "unique_tags_generated": len(tag_frequency),
            "average_tags_per_product": f"{len(all_tags)/len(products_with_tags):.1f}" if products_with_tags else "0",
            "most_common_tags": dict(tag_frequency.most_common(10)),
            "tag_categories_found": {
                "health_related": len([tag for tag in tag_frequency if any(keyword in tag for keyword in ['health', 'support', 'care'])]),
                "dietary": len([tag for tag in tag_frequency if any(keyword in tag for keyword in ['protein', 'grain', 'vegan', 'organic'])]),
                "life_stage": len([tag for tag in tag_frequency if any(keyword in tag for keyword in ['puppy', 'adult', 'senior', 'kitten'])])
            }
        }
    }