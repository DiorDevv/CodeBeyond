from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from maxsulot.models import Product, Comment, MaxsulotLike, CommentLike
from maxsulot.permessions import IsSuperUser
from maxsulot.serializers import ProductSerializer, CommentSerializer, CommentLikeSerializer, PostLikeSerializer


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Product successfully updated",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Product successfully deleted",
            }
        )


class ProductLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['id']
        return MaxsulotLike.objects.filter(product_id=product_id)


"------------------------------------------------------------------"


class ProductCommentListApiViews(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['id']
        return Comment.objects.filter(product_id=product_id)


class ProductCommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['id']
        product = Product.objects.get(id=product_id)
        serializer.save(author=self.request.user, product=product)





class CommentDetailApiView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()


class CommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return CommentLike.objects.filter(comment_id=comment_id)
