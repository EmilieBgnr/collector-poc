from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, condecimal
from typing import Optional
import uuid
import os

app = FastAPI(title="Collector.shop API")

ARTICLES_DB = {}
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

class Article(BaseModel):
    id: str
    title: str
    description: str
    price: condecimal(gt=0)
    category: str
    status: str = "PENDING_VALIDATION"
    image_path: Optional[str] = None

@app.post("/articles", response_model=Article, status_code=201)
async def create_article(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...)
):
    if image.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    article_id = str(uuid.uuid4())
    image_filename = f"{article_id}_{image.filename}"
    image_path = os.path.join(MEDIA_DIR, image_filename)

    with open(image_path, "wb") as f:
        f.write(await image.read())

    article = Article(
        id=article_id,
        title=title,
        description=description,
        price=price,
        category=category,
        image_path=image_path,
    )
    ARTICLES_DB[article_id] = article
    return article

@app.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    article = ARTICLES_DB.get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
