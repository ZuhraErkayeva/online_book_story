from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from .models import Author,Book,Order,OrderItem


class AuthorSerializers(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['name','birth_date','biography','books_count']

    def get_books_count(self,obj):
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializers(read_only=True)
    is_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title','author','isbn','price','stock','is_in_stock']


    def get_is_in_stock(self,obj):
        if obj.stock > 0:
            return True
        return False

    def validate_isbn(self, isbn):
        if len(isbn) != 13:
            raise serializers.ValidationError("Isbn must be 13 digits long.")
        if not isbn.isdigit():
            raise ValueError("ISBN must contain only numeric characters.")
        return isbn

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['book','quantity','subtotal']


    def get_subtotal(self,obj):
        quantity = obj.get_books_count()
        subtotal = obj.book.price * quantity
        return subtotal

    def validate_quantity(self, quantity):
        if quantity < 1:
            raise serializers.ValidationError("Quantity must be greater than or equal to 1.")
        return quantity


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.username')
    books = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['user','books','created_at','total_price']

    # umumiy narx
    def get_total_price(self, obj):
        return sum(item.subtotal for item in obj.items.all())

    def validate_books(self, books):
        # Har bir kitobni tekshirish
        for item in books:
            book = item['book']  # OrderItemSerializerdan kitobni olish
            book_quantity = item['quantity']  # Buyurtmalar soni

            # Kitobning necta borligini tekshirish
            book_instance = Book.objects.get(id=book)

            if book_instance.quantity < book_quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {book_instance.title}. There are only {book_instance
                    }")
        return books