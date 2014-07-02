# Ivelum task job
REST service for create async tasks

##  Description
несколько слов о самом решении. Для хранения результатов использую sqllite db (которую также залили в репозиторий). Сперва решил использовать постгрес, всё поставил, настроил поиспользовал, но потом понял, что проще будет передать решение с локальной бд - посему перешел на sqllite. Джанго обрабатывает запросы на создание задач и получении информации о них. Сами задачи выполняются в отдельными воркерами. Для этого использую redis-queue. Рассматривал вариант celery, но отказался из-за избыточной для этого проекта громоздкости. В качестве брокера выступает (как уже понятно) редис. Тут есть нюанс, что редис хранит модель данных в памяти и если у нас будет слишком много всяких очередей, которые не будут помещаться в память, то всё это дело загонит сервер в своп. Можно было использовать RabbitMQ, который складывает данные на диск и всё это оттуда постепенно подаёт и соответственно лишён, описываемого выше, недостатка, но он требует некой начальной конфигурации поэтому опять таки в пользу простоты передачи решение от меня вам и поднятия его решил использовать редис. Также был вариант написать свой велосипед с LPUSH и BRPOP на базе редиса, но потом решил отказаться от такого поступка.

В системе пользователю можно привязать несколько воркеров, что позволяет внедрить, например, систему разделения ресурсов машины в зависимости от того какой тариф оплатил (или не оплатил юзер). Т.е., например, во free версии юзеру привызяывается 1 дефаулт воркер, а тому кто купил какой-то тариф два (например) 1 hitgh priority и 1 дефолтный.
На данный момент выбрана самая простейшая модель определения какой воркер использовать для текущей задачи юзера - случайным образом выбирается конфигурации воркера (если их привязано 2 и более)

Для запуска системы по-мимо, установки библиотек, описанных, в requirement.txt необходимо установить redis-server, а также запустить воркеры (1 или несколько), например. команда:

```
python manage.py rqworker high normal low
```

Запускает 1 воркер, который будет обрабатывать всю очередь задач со всеми приоритетами.

Кроме этого, в проекте использутеся django-restframework для упрощения  построения REST api сервиса. Для реализации возможности производить кросс-доменные запросы было добавлен пакет django-cors-headers, который просто добавляет необходимые заголовки в ответ.

##  Замечания
1. Файл db.sqlite3 залит в репозитарий только из соображений удобства развёртывания тестового задания. Чтобы git clone и код + бд уже готовы к работе
2. По-хорошему, нужно создать local_settings.py и local_settings.py.example, вынести туда настройки, которые меняются от машины к машине и local_settings.py добавить в .gitigonre + импортировать его в settings. Но т.к. этот проект точно никто больше разрабатывать не будет и, более того первоначально, я даже не думал, что он будет размещен на github, то оставил просто settings.py
3. Данные, существующих в бд, пользователей: test:test, user1:user1, flashnot:zxc

##  How-to
you can:

    GET /api/v1/task - Get all my task
    POST* /api/v1/task - Create new tasks
    GET /api/v1/task/{id} - View task detail
    GET /api/v1/task/{id}/status - View task status
    GET /api/v1/task/{id}/result - View task result

, or Logout

* You must send post request with one require parameter - `input_param`. `input_param` is present pseudo input information for task worker.
For example start/create one (in second example three) task with bash and curl:

```
curl -X POST http://yourhost/api/v1/task/ -d "input_param=qwerty" -u test:test
curl -X POST http://yourhost/api/v1/task/ -d "input_param[]=asd&input_param[]=zxc&input_param[]=123" -u test:test
```

Or with jQuery:

```javascript
var username = 'test';
var password = 'test';

function make_base_auth(user, password) {
  var tok = user + ':' + password;
  var hash = btoa(tok);
  return "Basic " + hash;
}
$.ajax
  ({
    type: "POST",
    url: "http://yourhost/api/v1/task/",
    dataType: 'json',
    async: false,
    data: 'input_param=ZZZ',
    beforeSend: function (xhr){
        xhr.setRequestHeader('Authorization', make_base_auth(username, password));
    },
    success: function (){
        alert('OK!');
    }
});
```
            
