from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from transformers import pipeline
from langgraph.graph import Graph

# Database setup
DATABASE_URL = "mysql+pymysql://root:pranali@localhost:3306/chatbot_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
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

# LLM setup (using T5 or Bart would give better summarization results)
summarizer = pipeline("summarization", model="gpt2")

# FastAPI app
app = FastAPI()

# LangGraph nodes
def fetch_products(query: str):
    with SessionLocal() as db:
        products = db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
    return products

def fetch_suppliers(query: str):
    with SessionLocal() as db:
        suppliers = db.query(Supplier).filter(Supplier.product_categories_offered.contains(query)).all()
    return suppliers

def summarize_supplier(supplier: Supplier):
    summary = summarizer(supplier.contact_info, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

# LangGraph workflow
graph = Graph()

graph.add_node("fetch_products", fetch_products)
graph.add_node("fetch_suppliers", fetch_suppliers)
graph.add_node("summarize_supplier", summarize_supplier)

graph.add_edge("fetch_products", "summarize_supplier")
graph.add_edge("fetch_suppliers", "summarize_supplier")

# API endpoints
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def handle_query(request: QueryRequest):
    query = request.query.lower()
    if "product" in query:
        result = graph.run("fetch_products", query)
    elif "supplier" in query:
        result = graph.run("fetch_suppliers", query)
    else:
        raise HTTPException(status_code=400, detail="Invalid query")
    return {"response": result}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
