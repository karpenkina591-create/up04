from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Order
from .forms import OrderForm
from .serializers import OrderSerializer
from apps.catalog.models import Car


# ==========================================
# ЧАСТЬ 1: API (для дашборда и Streamlit)
# ==========================================
class OrderViewSet(viewsets.ModelViewSet):
    """CRUD для заказов (API)."""
    queryset = Order.objects.select_related("client", "car", "manager").all()
    serializer_class = OrderSerializer


# ==========================================
# ЧАСТЬ 2: Обычные веб-страницы (HTML)
# ==========================================

@login_required
def order_list(request):
    """Список всех заказов."""
    orders = Order.objects.select_related("client", "car", "manager").all()
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    """Детали конкретного заказа."""
    order = get_object_or_404(Order, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_create(request):
    """Создание нового заказа."""
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.manager = request.user  # Автоматически ставим текущего менеджера
            order.save()
            messages.success(request, "Заказ успешно создан!")
            return redirect("orders:order_list")
    else:
        form = OrderForm()
    
    return render(request, "orders/order_form.html", {"form": form})


@login_required
def order_complete(request, pk):
    """Завершение заказа (каскадно меняет статус авто на 'Продан')."""
    order = get_object_or_404(Order, pk=pk)
    order.complete()
    messages.success(request, f"Заказ #{order.pk} завершён.")
    return redirect("orders:order_detail", pk=pk)


@login_required
def order_cancel(request, pk):
    """Отмена заказа (каскадно возвращает авто в 'В наличии')."""
    order = get_object_or_404(Order, pk=pk)
    order.cancel()
    messages.warning(request, f"Заказ #{order.pk} отменён.")
    return redirect("orders:order_detail", pk=pk)