from django.core.cache import cache
from rest_framework import generics
from rest_framework.permissions import AllowAny

from django_design_pattern_app.api.v1.users.users import BaseView
from django_design_pattern_app.injector.base_injector import BaseInjector
from django_design_pattern_app.middleware.exceptions import handle_exceptions
from django_design_pattern_app.middleware.response import APIResponse
from django_design_pattern_app.models import Category, Product
from django_design_pattern_app.modules.procat_search_module import CatalogSearchELK


class CatalogSearchView(BaseView, generics.GenericAPIView):
    permission_classes = [AllowAny]

    # @handle_exceptions
    def post(self, request):
        q = request.data.get('q', '')
        cache_key = f"catalog_search:{q}"

        cached = cache.get(cache_key)
        if cached is not None:
            return APIResponse(data=cached, success_code=2000)

        es = BaseInjector.get(CatalogSearchELK)
        result = es.search(query={
            "multi_match": {
                "query": q,
                "fields": ["name^2", "slug^4", "description", "category_name", "path", "category_slug^4"]
            }
        })

        expanded = list(result['hits']['hits'])
        seen = {hit['_id'] for hit in expanded}

        for hit in result['hits']['hits']:
            source = hit['_source']
            if source.get('type') == 'category':
                slug = source.get('slug')
                try:
                    category = Category.objects.get(slug=slug)
                    all_ids = _get_all_descendant_ids(category.id)
                    products = Product.objects.filter(category_id__in=all_ids)
                    for p in products:
                        es_id = f"p_{p.id}"
                        if es_id not in seen:
                            seen.add(es_id)
                            expanded.append({
                                "_index": "catalog_index",
                                "_type": "_doc",
                                "_id": es_id,
                                "_score": hit['_score'],
                                "_source": {
                                    "id": p.id,
                                    "type": "product",
                                    "name": p.name,
                                    "slug": p.slug,
                                    "description": p.description,
                                    "price": float(p.price) if p.price else None,
                                    "category_slug": p.category.slug,
                                    "category_name": p.category.name,
                                }
                            })
                except Category.DoesNotExist:
                    pass

        cache.set(cache_key, expanded, timeout=300)
        return APIResponse(data=expanded, success_code=2000)


def _get_all_descendant_ids(category_id):
    ids = [category_id]
    children = Category.objects.filter(parent_id=category_id).values_list('id', flat=True)
    for child_id in children:
        ids.extend(_get_all_descendant_ids(child_id))
    return ids
