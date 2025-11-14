import os
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/listings")
def get_listings():
    """Mock listings endpoint returning a realistic set of Pokémon card deals."""
    base_time = datetime.utcnow()
    data = [
        {
            "id": "1",
            "name": "Charizard Holo 1st Edition",
            "price": 1899.99,
            "grade": "PSA 9",
            "supply": 12,
            "listed_at": (base_time - timedelta(minutes=3)).isoformat() + "Z",
            "marketplace": "eBay",
            "marketplace_url": "https://www.ebay.com/itm/charizard-1st-edition",
            "image_url": "https://images.pokemontcg.io/base2/4_hires.png",
            "alt_value": 2300.0,
            "difference": round(((2300.0 - 1899.99) / 2300.0) * 100, 2),
            "cartel_category": "Gold"
        },
        {
            "id": "2",
            "name": "Pikachu Illustrator",
            "price": 89999.0,
            "grade": "PSA 7",
            "supply": 1,
            "listed_at": (base_time - timedelta(minutes=12)).isoformat() + "Z",
            "marketplace": "Heritage",
            "marketplace_url": "https://www.ha.com/",
            "image_url": "https://images.pokemontcg.io/swsh35/12_hires.png",
            "alt_value": 110000.0,
            "difference": round(((110000.0 - 89999.0) / 110000.0) * 100, 2),
            "cartel_category": "Gold"
        },
        {
            "id": "3",
            "name": "Blastoise Shadowless",
            "price": 650.0,
            "grade": "BGS 9.5",
            "supply": 6,
            "listed_at": (base_time - timedelta(minutes=25)).isoformat() + "Z",
            "marketplace": "TCGPlayer",
            "marketplace_url": "https://www.tcgplayer.com/",
            "image_url": "https://images.pokemontcg.io/base1/2_hires.png",
            "alt_value": 710.0,
            "difference": round(((710.0 - 650.0) / 710.0) * 100, 2),
            "cartel_category": "Silver"
        },
        {
            "id": "4",
            "name": "Mewtwo EX",
            "price": 95.0,
            "grade": "Raw",
            "supply": 123,
            "listed_at": (base_time - timedelta(minutes=55)).isoformat() + "Z",
            "marketplace": "eBay",
            "marketplace_url": "https://www.ebay.com/",
            "image_url": "https://images.pokemontcg.io/bw3/54_hires.png",
            "alt_value": 85.0,
            "difference": round(((85.0 - 95.0) / 85.0) * 100, 2),
            "cartel_category": "Bronze"
        },
        {
            "id": "5",
            "name": "Gengar VMAX Alt Art",
            "price": 320.0,
            "grade": "PSA 10",
            "supply": 18,
            "listed_at": (base_time - timedelta(minutes=5)).isoformat() + "Z",
            "marketplace": "Mercari",
            "marketplace_url": "https://www.mercari.com/",
            "image_url": "https://images.pokemontcg.io/swsh8/271_hires.png",
            "alt_value": 380.0,
            "difference": round(((380.0 - 320.0) / 380.0) * 100, 2),
            "cartel_category": "Silver"
        }
    ]
    return data

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
