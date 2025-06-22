from django.urls import path

from maxsulot.views import ProductListView, ProductCreateView, ProductRetrieveUpdateDestroyAPIView, \
    ProductCommentListApiViews, \
    ProductCommentCreateView, ProductLikeListView, CommentDetailApiView, CommentLikeListView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-update-delete'),
    path('<int:id>/like', ProductLikeListView.as_view(), name='product-like'),
    path('<int:id>/comments/', ProductCommentListApiViews.as_view(), name='comment-list'),
    path('<int:id>/commet-create/', ProductCommentCreateView.as_view(), name='comment-create'),
    
    path('comment/<int:pk>/', CommentDetailApiView.as_view(), name='comment-detail'),
    path('comment/<int:id>/like', CommentLikeListView.as_view(), name='comment-like'),
]
