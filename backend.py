from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import logging
import pymysql  # Required for MySQL connection

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Database Configuration
DATABASE_URL = "mysql+pymysql://root:pranali@localhost:3306/chatbot_db"
engine = create_engine(DATABASE_URL, echo=True)  # Logs all SQL queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Define Database Models
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255))
    price = Column(Float)
    category = Column(String(255))
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(Text)
    product_categories_offered = Column(JSON)

# ✅ Create Tables in Database
Base.metadata.create_all(bind=engine)

# ✅ FastAPI App Initialization
app = FastAPI()

# ✅ Add CORS Middleware (Allows Frontend to Access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# ✅ Dependency for Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Define Request Model
class QueryRequest(BaseModel):
    query: str

# ✅ API Route for Querying Products
@app.post("/query")
def handle_query(request: QueryRequest, db: Session = Depends(get_db)):
    query = request.query.lower()
    logger.info(f"🔍 User Query: {query}")  

    try:
        # Fetch All Products (Debugging)
        all_products = db.query(Product).all()
        logger.info(f"✅ Total Products in DB: {len(all_products)}")

        # Extract Brand or Product Name from Query
        if "brand" in query:
            brand_name = query.split("brand")[-1].strip()
            logger.info(f"🔍 Extracted Brand: {brand_name}")

            filtered_products = db.query(Product).filter(Product.brand.ilike(f"%{brand_name}%")).all()
        
        elif "product" in query:
            product_name = query.replace("show me all", "").replace("products", "").strip()
            logger.info(f"🔍 Extracted Product Name: {product_name}")

            filtered_products = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).all()
        
        else:
            return {"response": "Invalid query format."}

        # Check if Products Exist
        if not filtered_products:
            return {"response": "No matching products found."}

        return {
            "response": [
                {"id": p.id, "name": p.name, "brand": p.brand, "price": p.price, "category": p.category}
                for p in filtered_products
            ]
        }

    except Exception as e:
        logger.error(f"❌ Database Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Home Route for API Status
@app.get("/")
def home():
    return {"message": "Welcome to AI Chatbot API!"}

# ✅ Run Server (Uncomment if running directly)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
