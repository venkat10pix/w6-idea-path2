from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import init_db, get_db, Idea

# Automatically create tables on startup
init_db()

app = FastAPI(title="Idea Tracker API")

class IdeaCreate(BaseModel):
    title: str
    description: str | None = None

class IdeaResponse(BaseModel):
    id: int
    title: str
    description: str | None = None

    model_config = {"from_attributes": True}

@app.post("/ideas", response_model=IdeaResponse)
def create_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    db_idea = Idea(title=idea.title, description=idea.description)
    db.add(db_idea)
    db.commit()
    db.refresh(db_idea)
    return db_idea

@app.get("/ideas", response_model=List[IdeaResponse])
def get_ideas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ideas = db.query(Idea).offset(skip).limit(limit).all()
    return ideas

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
