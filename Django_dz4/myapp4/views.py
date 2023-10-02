from django.shortcuts import render, redirect
import logging
from django.views import View
from .models import Client, Order
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    """
    Функция - заглушка. Если вызов был без параметров.
    :param request:
    :return:
    """
    logger.info('Index page accessed! Redirect to /lastday/0/7')
    return redirect("/lastday/0/7")


class LastDay(View):
    """
    Класс - форма вывода содержимого базы данных по запросу
    """
    def get(self, request, client_id, days=1):
        """
        :param request: django объект - запрос
        :param client_id: ID клиента, по которому выводим информацию
        :param days: - количество дней, за которые ищем заказы
        :return:
        """

        # Проверяем наличие клиента в базе, по которому передели client_id
        if client_id == 0:
            try:
                client_id = list(Client.objects.values_list('id', flat=True))[0]
            except IndexError:
                client_id = None

        # Запрос в базу данных, в соответствие с заданием:
        #   список заказанных клиентом товаров из всех его заказов с
        #   сортировкой по времени (7, 30, 365 дней)
        orders = ((Order.objects
                  .filter(client_id=client_id, order_date__gte=datetime.now(tz=timezone.utc) - timedelta(days=days)))
                  .distinct()
                  .order_by("order_date")
                  )

        context = {'orders': orders,
                   'client_id': client_id,
                   'clients': Client.objects.all(),  # Так же - отправляем всю базу клиентов в drop-down спискок
                   'days': days,
                   }
        return render(request, 'myapp4/orders.html', context)
