# DJANGO_JSON_RPC TEST_TASK
В тестовом задании требовалось создать примитивный web-клиент к существующему jsonrpc-сервису, пройти авторизацию на нём с помощью приложенного сертификата и ключа, получить данные и отобразить ответы.

Был создан **джанго-проект**:

Проинициализирована БД

В **settings.py**:
1. Настроен путь до '**/templates**/'
2. Добавлены переменные **CERTIFICATE**, **PRIVATE_KEY**, **JSONRPC_ENDPOINT**
3. Подключено приложение **json_rpc**

Создано приложение **json_rpc**:
1. Внутри папка **path**, которая хранит сертификаты и ключи
2. Добавлен модуль **forms.py**, чтобы удобно получить значения с html
3. Добавлен модуль **json_client.py**, где определена логика создания исключений и объекта класса **JSONRPCClient** (_создание ssl-сертификата, проверка на подлинность, загрузка сертификата, отправка POST-запроса с JSON RPC данными_)
4. **views.py**:
    1. Классовое представление функции, внутри которого достаются данные со страницы **HTML**, создается объект **JSONRPCClient** и отправляется запрос
   2. Также все внутри блока **try**/**except**, отлавливаем ошибки и выводим их


<p>
   <img width="300" src="https://github.com/pinkpipe/djangoJSONTEST/json_rpc/path/img/img_test.png">
</p>


# ТРУДНОСТИ

Во время решения этого тестового задания возникла проблема:

Внутри модуля json_client.py во время создания ssl-соединения - ваш сертификат не проходил проверку (возникало две ошибки либо что этот сертификат не является корневым, либо не подлинным).
Решил отключить проверку на подлинность по хосту и сертификату, но вытекали другие проблемы (без проверки были трудности загрузить сертификат)

Было принято решение зайти на **slb.medv.ru** и вручную получить корневой сертификат **ISRG Root X1.crt** - поместить его в наш проект и подгружать его

Все исправно заработало!!!