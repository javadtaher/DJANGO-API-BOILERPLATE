from typing import Type
from pydantic import BaseModel
from django_design_pattern_app.schemas.procat import CatalogIndexModel


class CatalogIndexConfig:
    es_index_name = "catalog_index"
    pydantic_model: Type[BaseModel] = CatalogIndexModel
    es_index_mapping = {
        "properties": {
            "id": {"type": "integer"},
            "type": {"type": "keyword"},
            "name": {"type": "text"},
            "slug": {"type": "keyword"},
            "description": {"type": "text"},
            "price": {"type": "float"},
            "category_slug": {"type": "keyword"},
            "category_name": {"type": "text"},
            "parent_slug": {"type": "keyword"},
            "path": {"type": "text"},
        }
    }
    es_settings = {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }