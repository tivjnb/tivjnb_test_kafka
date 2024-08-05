<h1>Это решение старого задания</h1>
ТЗ было таким:
<div>Необходимо реализовать микросервис взаимодействия с очередью
rest интерфейс

1. /queue/set_data
POST
запись данных в очередь
входные параметры
{"receiver_id': string, 'sender_id': string, 'data': json}

данные data записывается в kafka в очередь с topic: 'asutk_ms_{receiver_id}'

2. /queue/get_data?receiver_id=receiver_id
GET
отдает данные из очереди с учетом topic по значению receiver_id 'asutk_ms_{receiver_id}', только последние данные
в формате json {'data': data}
</div>

<h2>Соответственно это и делает мой код, но как мне кажется очень неправильно)</h2>
