from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from faiss_crud import faiss_crud

app = FastAPI()

class Item(BaseModel):
    id: int
    text: str

@app.post("/create")
async def create_item(item: Item):
    try:
        faiss_crud.create(item.id, item.text)
        return {"message": "Item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/read")
async def read_item(text: str, k: int = 1):
    try:
        distances, indices = faiss_crud.read(text, k)
        return {"distances": distances.tolist(), "indices": indices.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/update")
async def update_item(item: Item):
    try:
        faiss_crud.update(item.id, item.text)
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete/{item_id}")
async def delete_item(item_id: int):
    try:
        faiss_crud.delete(item_id)
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
