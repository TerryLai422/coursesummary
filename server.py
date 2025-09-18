from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
def create_item(item: Item):
    if item.price < 0:
        raise HTTPException(status_code=400, detail="Price must be non-negative")
    data = item.dict()
    if item.tax is not None:
        data["total_price"] = item.price + item.tax
    return data

if __name__ == "__main__":
    uvicorn.run(
        "main:app",       # "module_name:app_instance"
        host="0.0.0.0",
        port=8000,
        reload=True       # auto-reloads on code changes
    )