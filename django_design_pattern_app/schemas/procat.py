from pydantic import BaseModel
from typing import Optional


class CatalogIndexModel(BaseModel):
    id: int
    type: str  # "product" or "category"
    name: str
    slug: Optional[str] = None

    # product
    description: Optional[str] = None
    price: Optional[float] = None
    category_slug: Optional[str] = None
    category_name: Optional[str] = None

    # category
    parent_slug: Optional[str] = None
    path: Optional[str] = None
