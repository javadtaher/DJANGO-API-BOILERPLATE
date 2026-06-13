from django.urls import path
from django_design_pattern_app.api.v1.products.products import CategoryTreeView, ManageProductView, ManageCategoryView

products_url = [
    path('products/<path:category_path>/', CategoryTreeView.as_view(), name='category_tree'),
    path('manage/category/', ManageCategoryView.as_view(), name='manage_category'),
    path('manage/product/', ManageProductView.as_view(), name='manage_product'),
]
