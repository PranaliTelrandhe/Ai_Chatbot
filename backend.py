from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List

# ? Database setup
DATABASE_URL = "mysql+pymysql://root:pranali@localhost:3306/chatbot_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ? Models
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(Text)
    product_categories_offered = Column(JSON)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255))
    price = Column(Float)
    category = Column(String(255))
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

Base.metadata.create_all(bind=engine)

# ? FastAPI App
app = FastAPI()

# ? Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # ? Allow all methods
    allow_headers=["*"],  
)

# ? Request Model
class QueryRequest(BaseModel):
    query: str

# ? API Endpoint
@app.post("/query")
def handle_query(request: QueryRequest):
    query = request.query.lower()
    db = SessionLocal()

    try:
        # Search for products
        if "products" in query:
            products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
            return {"response": [p.name for p in products]}

        # Search for suppliers
        elif "suppliers" in query:
            suppliers = db.query(Supplier).filter(Supplier.name.ilike(f"%{query}%")).all()
            return {"response": [s.name for s in suppliers]}

        else:
            return {"response": "No matching records found."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        db.close()
