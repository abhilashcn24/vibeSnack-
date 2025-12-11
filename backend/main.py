from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import model_utils
from database import get_snacks_collection, get_history_collection
import uvicorn
import os

app = FastAPI(title="VibeSnack API", root_path="/api" if os.environ.get("VERCEL") else "")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
model = model_utils.load_model()

class UserInput(BaseModel):
    hour: int
    mood: str
    hunger: int
    diet: str
    context: str

class Feedback(BaseModel):
    snack_id: int

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(input_data: UserInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Fetch data from DB
    try:
        snacks_col = get_snacks_collection()
        history_col = get_history_collection()
        
        snack_catalog = list(snacks_col.find({}, {"_id": 0}))
        
        history_doc = history_col.find_one({"_id": "global_history"})
        user_history = history_doc.get("counts", {}) if history_doc else {}
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback to empty if DB fails, or raise error
        # For demo purposes, let's try to load from local json if DB fails as fallback?
        # But we moved logic to DB. Let's just return error or empty.
        raise HTTPException(status_code=503, detail="Database unavailable")

    recommendations = model_utils.predict_snack(
        model, 
        input_data.dict(), 
        snack_catalog, 
        user_history, 
        top_k=5
    )
    
    # Add messages and explanations
    results = []
    for rec in recommendations:
        msg = model_utils.format_personalized_message(input_data.dict(), rec['name'])
        explanation = model_utils.generate_explanation(input_data.dict(), rec['snack_details'])
        
        results.append({
            "id": rec['id'],
            "name": rec['name'],
            "prob": rec['prob'],
            "tags": rec['tags'],
            "message": msg,
            "explanation": explanation
        })
        
    return {"recommendations": results}

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    history_col = get_history_collection()
    
    # Upsert global history
    # We store counts in a dict under "counts" field
    sid_str = str(feedback.snack_id)
    
    history_col.update_one(
        {"_id": "global_history"},
        {"$inc": {f"counts.{sid_str}": 1}},
        upsert=True
    )
    
    return {"status": "success", "message": "Feedback recorded"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
