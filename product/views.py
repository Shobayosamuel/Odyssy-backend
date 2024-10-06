from rest_framework import generics, response, status
from .models import Product, Category, Cart, CartItem
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CartItemSerializer,
    CartSerializer,
)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=request.data.get("product_id"))
        quantity = request.data.get("quantity", 1)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        # Update cart total
        cart.total += cart_item.get_total_item_price()
        cart.save()

        return response.Response({"message": "Added to cart"}, status=status.HTTP_200_OK)

