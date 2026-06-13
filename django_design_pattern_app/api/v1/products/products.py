import random

from rest_framework import generics
from rest_framework.permissions import AllowAny

from django_design_pattern_app.api.v1.users.users import BaseView
from django_design_pattern_app.middleware.exceptions import handle_exceptions
from django_design_pattern_app.middleware.response import APIResponse
from django_design_pattern_app.middleware.validate import validate_serializer
from django_design_pattern_app.models import Category, Product
from django_design_pattern_app.permissions.permissions import IsAuthenticated, IsAdminOrEditor

from django_design_pattern_app.serializers.product.product_serializers import ManageCategorySerializer, \
    ManageProductSerializer


class CategoryTreeView(BaseView, generics.GenericAPIView):
    permission_classes = [AllowAny]

    @handle_exceptions
    def get(self, request, category_path):
        slugs = [s for s in category_path.split('/') if s]

        parent = None
        for slug in slugs:
            try:
                parent = Category.objects.get(slug=slug, parent=parent)
            except Category.DoesNotExist:
                return APIResponse(data=f"category '{slug}' not found", error_code=1000, status=404)

        all_ids = self._get_all_descendant_ids(parent.id)
        products = Product.objects.filter(category_id__in=all_ids)

        return APIResponse(data={
            "category": parent.name,
            "products_count": products.count(),
            "products": [
                {"name": p.name, "price": str(p.price) if p.price else None}
                for p in products
            ]
        }, success_code=2000)

    def _get_all_descendant_ids(self, category_id):
        ids = [category_id]
        children = Category.objects.filter(parent_id=category_id).values_list('id', flat=True)
        for child_id in children:
            ids.extend(self._get_all_descendant_ids(child_id))
        return ids


class ManageCategoryView(BaseView, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEditor]
    serializer_class = ManageCategorySerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        action = request.data.get('action')
        slug = request.data.get('slug')

        if action == 'add':
            name = request.data.get('name')

            parent_slug = request.data.get('parent')
            parent = None
            if parent_slug:
                try:
                    parent = Category.objects.get(slug=parent_slug)
                except Category.DoesNotExist:
                    return APIResponse(
                        data="Parent category not found",
                        error_code=1, status=404
                    )

            Category.objects.create(name=name, slug=slug, parent=parent)
            return APIResponse(data="added", success_code=2000)

        elif action == 'delete':
            children = Category.objects.filter(parent__slug=slug)
            children.delete()

            try:
                category = Category.objects.get(slug=slug)
            except Category.DoesNotExist:
                return APIResponse(data="Category not found", error_code=1, status=404)

            category.delete()
            return APIResponse(data="deleted", success_code=2000)

        return APIResponse(data="unknown action", error_code=1, status=400)


class ManageProductView(BaseView, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrEditor]
    serializer_class = ManageProductSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        action = request.data.get('action')
        name = request.data.get('name')
        slug = request.data.get('slug')
        category_slug = request.data.get('category')
        description = request.data.get('description')
        price = request.data.get('price')

        if action == 'add':
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                return APIResponse(
                    data="Category not found",
                    error_code=1, status=404
                )
            proID = f"405{random.randint(0, 9999999999):010d}"
            Product.objects.create(
                product_id=proID,
                name=name, slug=f"{slug}_{proID}",
                category=category,
                description=description,
                price=price
            )
            return APIResponse(data=f"added {proID}", success_code=2000, status=200)

        elif action == 'delete':
            try:
                product = Product.objects.get(slug=slug)
            except Product.DoesNotExist:
                return APIResponse(
                    data="Product not found",
                    error_code=1, status=404
                )
            product.delete()
            return APIResponse(data="deleted", success_code=2000, status=200)

        return APIResponse(data="unknown action", error_code=1, status=400)
