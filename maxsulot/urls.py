from django.urls import path

from maxsulot.views import ProductListView, ProductCreateView, ProductRetrieveUpdateDestroyAPIView, CommentListApiViews, \
    CommentCreateView, ProductLikeListView, CommentRetrieveApiView

urlpatterns = [
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-update-delete'),
    path('<int:id>/comment-lists/', CommentListApiViews.as_view(), name='comment-list'),
    path('<int:id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:id>/like', ProductLikeListView.as_view(), name='product-like'),
    path('<int:pk>/commet', CommentRetrieveApiView.as_view(), name='comment'),

]
