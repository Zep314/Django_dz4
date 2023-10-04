from django.shortcuts import render, redirect
import logging
from django.views import View
from .models import Client, Order
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import ProductForm
from .models import Product
from django.core.files.storage import FileSystemStorage

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


class ProductView(View):
    """
    Класс для работы с формой создания/редактирования товара
    """
    def get(self, request):
        """
        Обработка формы при создании нового товара
        :param request:
        :return:
        """
        form = ProductForm(initial={'id': '0', 'name': '', 'description': '', 'price': 0, 'amount': 1})
        message = 'Заполните форму'
        return render(request, 'myapp4/product.html', {'form': form, 'message': message})

    def post(self, request):
        """
        Обработка формы при редактировании или сохранении данных
        :param request:
        :return:
        """
        if 'product_id' in request.POST:
            # Нажали кнопку РЕДАКТИРОВАТЬ - отображаем форму с редактируемыми данными

            # Вытаскиваем данные из базы данных
            product = Product.objects.filter(pk=request.POST['product_id']).first()
            initial = {'id': str(request.POST['product_id']),
                       'name': product.name,
                       'description': product.description,
                       'price': product.price,
                       'amount': product.amount,
                       'image': product.image,
                       }
            form = ProductForm(initial=initial)
            message = 'Измените данные'
            return render(request, 'myapp4/product.html', {'form': form, 'message': message})
        else:
            # Пытаемся сохранить данные из формы
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product_id = form.cleaned_data['id']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                amount = form.cleaned_data['amount']
                image = form.cleaned_data['image']
                fs = FileSystemStorage()
                logger.info(f'Image: {image.name=}')
                fs.save(image.name, image)

                if product_id == 0:
                    # Вновь создаваемый товар
                    product = Product(name=name, description=description,
                                      price=str(price), amount=amount, image=image.name)
                else:
                    # Изменение данных уже существующего товара
                    product = Product.objects.filter(pk=product_id).first()
                    product.name = name
                    product.description = description
                    product.price = price
                    product.amount = amount
                    product.image = image.name
                product.save()
                logger.info(f'Successfully create product: {product}')
                return redirect("/lastday/0/7")  # Переходим к таблице заказов
            else:
                # если ошибка (или валидация не пройдена) - заново отображаем форму, с уже заполненными данными
                message = 'Ошибка в данных'
                return render(request, 'myapp4/product.html', {'form': form, 'message': message})
