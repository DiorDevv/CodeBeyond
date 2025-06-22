from rest_framework import serializers

from users.models import CustomUser
from users.serializers import UserSerializer
from .models import Product, Category, Comment, MaxsulotLike, CommentLike


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    # Write uchun category faqat id-larni qabul qiladi
    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    # name, description, image — o'qish va yozishda ko'rinadigan qilib
    name = serializers.CharField()
    description = serializers.CharField()
    image = serializers.ImageField(required=False)

    post_likes_count = serializers.SerializerMethodField()
    post_comments_count = serializers.SerializerMethodField()
    me_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            'author',
            'name',
            'description',
            'image',
            'created_at',
            "post_likes_count",
            "post_comments_count",
            "me_liked",
            'category'
        ]
        extra_kwargs = {"image": {"required": False}}

    @staticmethod
    def get_post_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_post_comments_count(obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                MaxsulotLike.objects.get(product=obj, author=request.user)
                return True
            except MaxsulotLike.DoesNotExist:
                return False

        return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    me_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'like_count', 'parent', 'replies', 'product', 'me_liked']
        extra_kwargs = {"parent": {"required": False}}

    def get_replies(self, obj):
        if hasattr(obj, 'child') and obj.child.exists():
            serializer = CommentSerializer(obj.child.all(), many=True, context=self.context)
            return serializer.data
        return None

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        return False

    def get_like_count(self, obj):
        return obj.likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ("id", "author", "comment")


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = MaxsulotLike
        fields = ("id", "author", "product")


class bwibf:
    pass
