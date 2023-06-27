from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from common.views import TitleMixin
from orders.forms import OrderForm


""" Контроллер создания заказа """


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
