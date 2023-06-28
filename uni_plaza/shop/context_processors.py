from shop.models import Basket


def baskets(request):  # Контекстный процессор (переменная 'baskets' теперь глобальная)
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
