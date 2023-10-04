# Фреймворк Django (семинары)
## Урок 4. Работа с пользователями и права в Django. Оптимизация проекта

### Задание 1

Измените модель продукта, добавьте поле для хранения фотографии продукта.

Создайте форму, которая позволит сохранять фото.


<details>
<summary> Задание у уроку 2: </summary>
---=== Урок 2 ===---


Создайте три модели Django: клиент, товар и заказ.

Клиент может иметь несколько заказов. Заказ может содержать несколько товаров. Товар может входить в несколько заказов.

Поля модели «Клиент»:
— имя клиента
— электронная почта клиента
— номер телефона клиента
— адрес клиента
— дата регистрации клиента

Поля модели «Товар»:
— название товара
— описание товара
— цена товара
— количество товара
— дата добавления товара

Поля модели «Заказ»:
— связь с моделью «Клиент», указывает на клиента, сделавшего заказ
— связь с моделью «Товар», указывает на товары, входящие в заказ
— общая сумма заказа
— дата оформления заказа

Допишите несколько функций CRUD для работы с моделями по желанию. Что по вашему мнению актуально в такой базе данных.
</details>

<details>
<summary> Задание у уроку 3: </summary>


---=== Урок 3 ===---

Продолжаем работать с товарами и заказами.

Создайте шаблон, который выводит список заказанных клиентом товаров из всех его заказов с 
сортировкой по времени:

- за последние 7 дней (неделю)
- за последние 30 дней (месяц)
- за последние 365 дней (год)

Товары в списке не должны повторятся.

==========================
</details>

### Решение

<details>
<summary>Повторяем действия для создания приложения:</summary>
Выполняем стандартные процедуры для запуска нового приложения в новом проекте:

Устанавливаем Django:

    pip install django

Создаем проект для работы:

    django-admin startproject Django_dz4

Переходим в папку проекта:

    cd .\Django_dz4\

Создаем новое приложение в проекте:

    python manage.py startapp myapp4

Запускаем сервер проекта:

    python manage.py runserver

Редактируем файлы:

- [Django_dz4/Django_dz4/Django_dz4/settings.py](/Django_dz4/Django_dz4/settings.py)
- [Django_dz4/Django_dz4/Django_dz4/urls.py](/Django_dz4/Django_dz4/urls.py)
- [Django_dz4/Django_dz4/myapp4/urls.py](/Django_dz4/myapp4/urls.py)
- [Django_dz4/Django_dz4/myapp4/views.py](/Django_dz4/myapp4/views.py)

Создаем модель данных, в соответствие с заданием. 
Модель данных находится в файле: 

- [Django_dz4/Django_dz4/myapp4/models.py](/Django_dz4/myapp4/models.py)

Для каждой таблицы были реализованы все **CRUD** методы. Для таблицы заказов (Order) выполнена поддержка связи 
Many-to-Many с таблицей товаров (Product). 

Примеры методов находятся в пакете *commands*:

- [Django_dz4/Django_dz4/myapp4/management/commands/](/Django_dz4/myapp4/management/commands)

Создаем миграции для нашей модели данных (подготавливаем структуру базы данных для развертывания на сервере БД):

    python manage.py makemigrations myapp4

Применяем миграции (Физически создаем объекты на сервере БД):

    python manage.py migrate

После этого можно запускать команды для работы нашей модели с базой данных:

    python manage.py create_client.py
    python manage.py create_order.py
    python manage.py create_product.py
    python manage.py get_client.py 1
    python manage.py get_order.py 3
    python manage.py get_product.py 1
    python manage.py update_client.py 1
    python manage.py update_order.py 1
    python manage.py update_product.py 1
    python manage.py get_all_clients.py
    python manage.py get_all_orders.py
    python manage.py get_all_products.py
    python manage.py delete_client.py 2
    python manage.py delete_order.py 2
    python manage.py delete_product.py 2


Файл с журналом работы:

- [logs/django.log](/Django_dz4/logs/django.log) 

Для более удобной работы был написан генератор фейковых данных
 
- [Django_dz4/Django_dz4/myapp4/management/commands/gen_fake_data.py](/Django_dz4/myapp4/management/commands/gen_fake_data.py)

        python manage.py gen_fake_data.py 50 50 200

В файле представлений описан запрос в базу данных и вызов формы представления данных по запросу

- [Django_dz4/Django_dz4/myapp4/views.py](/Django_dz4/myapp4/views.py)

Так же были подготовлены шаблоны для отображения формы. Файлы с шаблонами:

- [Django_dz4/Django_dz4/myapp4/templates/myapp4/base.html](/Django_dz4/myapp4/templates/myapp4/base.html)
- [Django_dz4/Django_dz4/myapp4/templates/myapp4/menu.html](/Django_dz4/myapp4/templates/myapp4/menu.html)
- [Django_dz4/Django_dz4/myapp4/templates/myapp4/orders.html](/Django_dz4/myapp4/templates/myapp4/orders.html)

Для более эстетичного восприятия был добавлен [bootstrap](https://getbootstrap.com/)

</details>

Так же - изменяем модель данных - добавляем поле для хранения имени файла-изображения для товара.
Поле может принимать значение NULL, что указываем в модели данных. Не забываем сделать миграцию.

- [Django_dz4/Django_dz4/myapp4/models.py](/Django_dz4/myapp4/models.py)

Так же - создаем папку для хранения изображений, и указываем ее в настройках 

- [Django_dz4/Django_dz4/Django_dz4/settings.py](/Django_dz4/Django_dz4/settings.py)


        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'myapp4/media'

        python manage.py gen_fake_data.py 50 50 200

В файле *urls.py* указываем маршруты к новой форме редактирования товара, и к папке, 
в которой хранятся изображения  

- [Django_dz4/Django_dz4/Django_dz4/urls.py](/Django_dz4/Django_dz4/urls.py)

Разрабатываем представление для формы создания/редактирования товара: 

- [Django_dz4/Django_dz4/myapp4/forms.py](/Django_dz4/myapp4/forms.py)

Разрабатываем шаблон для отображения формы создания/редактирования товара:

- [Django_dz4/Django_dz4/myapp4/templates/myapp4/product.html](/Django_dz4/myapp4/templates/myapp4/product.html)

В файле *views.py* описываем логику работы представления

- [Django_dz4/Django_dz4/myapp4/views.py](/Django_dz4/myapp4/views.py)

Прописываем маршрут и класс для отображения формы в файле *urls.py*

- [Django_dz4/Django_dz4/myapp4/urls.py](/Django_dz4/myapp4/urls.py)

## Результат работы:

Таблица заказов за 30 дней для определенного клиента:

![screen2.png](screen2.png)

Форма создания/редактирования товара с возможностью "привязать" изображение:

![screen1.png](screen1.png)
