from django.urls import path

from maxsulot.views import ProductListView, ProductCreateView, ProductRetrieveUpdateDestroyAPIView, CommentListApiViews, \
    CommentCreateView

urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-update-delete'),
    path('product/<int:id>/comments/', CommentListApiViews.as_view(), name='comment-list'),
    path('product/<int:id>/comments/create/', CommentCreateView.as_view(), name='product-create'),
]
