from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j_crud import Neo4jCRUD

app = FastAPI()

# Define the Person model
class Person(BaseModel):
    name: str
    age: int

# Initialize the Neo4jCRUD instance
db = Neo4jCRUD(uri="bolt://localhost:7687", user="neo4j", password="Nerogod3313")

@app.post("/persons/", response_model=Person)
def create_person(person: Person):
    created_person = db.create_person(person.name, person.age)
    return {"name": created_person["name"], "age": created_person["age"]}

@app.get("/persons/{name}", response_model=Person)
def read_person(name: str):
    person = db.get_person(name)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"name": person["name"], "age": person["age"]}

@app.put("/persons/{name}", response_model=Person)
def update_person(name: str, person: Person):
    updated_person = db.update_person(name, person.age)
    return {"name": updated_person["name"], "age": updated_person["age"]}

@app.delete("/persons/{name}")
def delete_person(name: str):
    db.delete_person(name)
    return {"detail": "Person deleted"}

@app.on_event("startup")
async def startup_event():
    # Code to run on startup
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Code to run on shutdown
    db.close()
