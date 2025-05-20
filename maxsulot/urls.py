from django.urls import path

from maxsulot.views import ProductListView, ProductCreateView

urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
]
