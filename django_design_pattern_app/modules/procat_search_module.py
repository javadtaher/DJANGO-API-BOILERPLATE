from injector import Module, singleton, provider
from elasticsearch import Elasticsearch
from django_design_pattern_app.services.redis.redis import RedisService
from django_design_pattern_app.services.elasticsearch.elasticsearch import SearchELK
from django_design_pattern_app.services.elasticsearch.indexing.procats_index import CatalogIndexConfig


class CatalogSearchELK(SearchELK, CatalogIndexConfig):
    pass


class CatalogSearchModule(Module):
    @singleton
    @provider
    def provide_catalog_search(self, es: Elasticsearch, redis: RedisService) -> CatalogSearchELK:
        return CatalogSearchELK(es=es, redis=redis)
