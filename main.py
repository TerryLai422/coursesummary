from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from document_loader import extract, save_text_to_file

app = FastAPI()

class Info(BaseModel):
    filename: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/extract-pdf/")
def extract_pdf(info: Info):
    try:
        texts = extract(info.filename)
        save_text_to_file(texts, info.filename)

    except Exception as e:
        print(f"[ERROR]: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    data = info.dict()
    return data

if __name__ == "__main__":
    uvicorn.run(
        "main:app",       # "module_name:app_instance"
        host="0.0.0.0",
        port=8000,
        reload=True       # auto-reloads on code changes
    )