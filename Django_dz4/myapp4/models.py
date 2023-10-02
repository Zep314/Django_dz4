from django.db import models

# Create your models here.


class Client(models.Model):
    """
    Описываем модель данных для работы с таблицей клиентов
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name: \'{self.name}\', email: {self.email}, phone: \'{self.phone}\', address: \'{self.address}\', ' \
                f'register_date: {self.register_date}'


class Product(models.Model):
    """
    Описываем модель данных для работы с таблицей товаров
    """
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name: \'{self.name}\' ,Description: \'{self.description}\' ,Price: {self.price:.2f} ' \
               f',Amount: {self.amount} ,Create_date: {self.create_date} '


class Order(models.Model):
    """
    Описываем модель данных для работы с таблицей заказов
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_date = models.DateTimeField()

    def __str__(self):
        return f'Client: {self.client}, Product[s]: {self.products.all().values_list()}' \
               f', Total price: {self.total_price:.2f} ,Order_date: {self.order_date}'
