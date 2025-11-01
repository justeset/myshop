from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from cart.models import Cart
from .models import Order, OrderItem
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(
            (Decimal(item.product.price) * item.quantity for item in cart.items.all()),
            Decimal('0')
        )

        if hasattr(user, 'profile') and Decimal(user.profile.balance) < total_price:
            return Response({'error': 'Недостаточно средств'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return Response(
                    {'error': f'Недостаточно товара {item.product.name} на складе'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(user=user)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock = max(item.product.stock - item.quantity, 0)
            if item.product.stock == 0:
                item.product.available = False
            item.product.save()

        if hasattr(user, 'profile'):
            user.profile.balance = Decimal(user.profile.balance) - total_price
            user.profile.save()

        cart.items.all().delete()

        logger.info(f'🧾 Новый заказ #{order.id} от пользователя {user.username}, сумма: {total_price}₽')

        return Response({'message': 'Заказ успешно создан', 'order_id': order.id})
