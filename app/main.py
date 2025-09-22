from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from app.database import Database, get_pet_profiles_collection, get_products_collection
from app.routes.pets import router as pets_router
from app.routes.recommendations import router as recommendations_router
from app.routes.products import router as products_router

# Create FastAPI app
app = FastAPI(
    title="Pet Product Recommendation API with ML Tag Generation", 
    version="4.0.0",
    description="Advanced pet product recommendations with ML-powered automatic tag generation",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files if directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Database lifecycle events
@app.on_event("startup")
def startup_db_client():
    Database.initialize()
    print("🤖 Pet Recommendation System with ML Tag Generation started!")
    print("📊 Admin Interface: http://localhost:8000/admin")

@app.on_event("shutdown")
def shutdown_db_client():
    Database.close_connection()
    print("👋 System shutdown complete!")

# Include routers
app.include_router(pets_router, prefix="/api/v1", tags=["pets"])
app.include_router(recommendations_router, prefix="/api/v1", tags=["recommendations"])
app.include_router(products_router, prefix="/api/v1", tags=["products"])

# Serve the product management UI
@app.get("/admin", response_class=HTMLResponse)
def serve_admin_ui():
    """Serve the product management interface"""
    template_path = os.path.join("templates", "admin.html")
    
    if not os.path.exists(template_path):
        return HTMLResponse("""
        <html>
            <body>
                <h1>Admin Template Not Found</h1>
                <p>Please create the templates/admin.html file.</p>
                <p>Template should be located at: templates/admin.html</p>
            </body>
        </html>
        """, status_code=404)
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except Exception as e:
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Error Loading Admin Interface</h1>
                <p>Error: {str(e)}</p>
            </body>
        </html>
        """, status_code=500)

# Root endpoints
@app.get("/")
def read_root():
    return {
        "message": "Pet Product Recommendation System with ML Tag Generation",
        "version": "4.0.0",
        "features": [
            "ML-Powered Auto Tag Generation",
            "Health Condition Priority (35%)",
            "Safety & Allergy Matching (30%)", 
            "General Compatibility (25%)",
            "Quality & Business Metrics (10%)",
            "Multi-Category Product Support"
        ],
        "ml_capabilities": [
            "Automatic tag generation for all product types",
            "Semantic understanding across categories",
            "Health-focused tag prioritization",
            "Explainable tag recommendations"
        ],
        "endpoints": {
            "admin_ui": "/admin",
            "pets": "/api/v1/pets/",
            "recommendations": "/api/v1/recommendations/",
            "products": "/api/v1/products/",
            "ml_preview": "/api/v1/products/preview-ml-tags",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    """System health check with ML capabilities"""
    try:
        pets_collection = get_pet_profiles_collection()
        pet_count = pets_collection.count_documents({})
        
        products_collection = get_products_collection()
        product_count = products_collection.count_documents({})
        products_with_ml_tags = products_collection.count_documents({"tags": {"$exists": True, "$ne": []}})
        
        return {
            "status": "healthy",
            "database": "connected",
            "pets_count": pet_count,
            "products_count": product_count,
            "products_with_ml_tags": products_with_ml_tags,
            "ml_tag_coverage": f"{(products_with_ml_tags/product_count*100):.1f}%" if product_count > 0 else "0%",
            "algorithm": "balanced_health_first_with_ml",
            "ml_features": {
                "tag_generation": True,
                "semantic_understanding": True,
                "multi_category_support": True,
                "health_prioritization": True
            },
            "scoring_weights": {
                "health_condition_match": "35%",
                "safety_allergy_match": "30%", 
                "general_compatibility": "25%",
                "quality_business": "10%"
            },
            "mvp_status": {
                "ready_for_testing": product_count >= 20,
                "ml_tag_ready": products_with_ml_tags >= 10,
                "recommendation": "Add more products with ML tags" if products_with_ml_tags < 10 else "Ready for ML-powered MVP"
            }
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)