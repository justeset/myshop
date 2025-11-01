from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from catalog.views import ProductViewSet, CategoryViewSet
from users.views import RegisterView, ProfileView, AddBalanceView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # JWT авторизация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Пользователи
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/profile/', ProfileView.as_view(), name='profile'),
    path('api/users/add-balance/', AddBalanceView.as_view(), name='add_balance'),

    # Каталог (товары + категории)
    path('api/catalog/', include(router.urls)),

    # Документация
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    #Корзина
    path('api/cart/', include('cart.urls')),
    
    #Заказы
    path('api/orders/', include('orders.urls')),
]
