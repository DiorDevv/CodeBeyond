from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models
from django.db.models import UniqueConstraint

from shared.restframework.models import BaseModel
from users.models import CustomUser


class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseModel):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='products', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ManyToManyField(Category, related_name='products')

    # created_at = models.DateTimeField(auto_now_add=True)
    # views = models.ManyToManyField(CustomUser, related_name='viewed_products', blank=True)
    # likes = models.ManyToManyField(CustomUser, related_name='liked_products', blank=True)

    class Meta:
        db_table = 'maxsulot_product'
        verbose_name = 'maxsulot_product'
        verbose_name_plural = 'maxsulot_product'

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='replies')

    def __str__(self):
        return f'{self.user.username} → {self.text[:30]}'


class MaxsulotLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'product'],
                name='product_like_unique'
            )
        ]


class CommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'comment'],
                name='comment_like_unique'
            )
        ]
