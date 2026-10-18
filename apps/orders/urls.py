"""МОДУЛЬ 4 (ЗАКАЗЫ): URL-маршруты."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import OrderViewSet

# 1. Настройка API (для дашборда и Streamlit)
router = DefaultRouter()
router.register("api", OrderViewSet, basename="orders-api")

app_name = "orders"

# 2. Настройка обычных веб-страниц
urlpatterns = [
    # API-пути (будут доступны по адресу /api/orders/api/)
    path("", include(router.urls)),

    # Веб-страницы (HTML)
    path("web/", views.order_list, name="order_list"),
    path("web/create/", views.order_create, name="order_create"),
    path("web/<int:pk>/", views.order_detail, name="order_detail"),
    path("web/<int:pk>/complete/", views.order_complete, name="order_complete"),
    path("web/<int:pk>/cancel/", views.order_cancel, name="order_cancel"),
]