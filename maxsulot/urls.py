from django.urls import path

from maxsulot.views import MaxsulotListCreateView, CommentListCreateAPIView

urlpatterns = [
    path('maxsulot/', MaxsulotListCreateView.as_view(), name='maxsulot-list-create'),
    path('products/<int:product_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),

]