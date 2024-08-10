# Задание 1

Написать скрипт на `python`, который на вход принимает `json`-строку вида:

```json
[
    {
        'begin': '0000-00-00 00:00:00',
        'end': '9999-12-31 23:59:59',
        'record_id': 1,
        'name': 'RecordOne'
    }, 
    {
        'begin': '2020-03-06 14:00:20',
        'end': '2021-12-03 23:59:50',
        'record_id': 2,
        'name': 'RecordTwo'
    }
]
```

Скрипт выводит информацию о том, какие записи закончат свое действие до конца текущего месяца. Вызов скрипта через консоль. Версия python - 3. В выводе должен присутствовать `record_id` и `name`, даты не обязательны.

---
## Реализация - `.\task_1`

### Использование

- Python - 3.X
- `pip install -r requirements.txt`


Для запуска скрипта через консоль выполнить команду:
```
python .\task_1\main.py -r="[{'begin': '2020-03-06 14:00:20', 'end': '2024-07-13 23:59:50', 'record_id': 1, 'name': 'RecordOne'}, {'begin': '2020-03-06 14:00:20', 'end': '2024-08-13 23:59:50','record_id': 2,'name': 'RecordTwo'}]" -p -d -m=0
```
или:
```
python .\task_1\main.py -r="[{'begin': '2020-03-06 14:00:20', 'end': '2024-07-13 23:59:50', 'record_id': 1, 'name': 'RecordOne'}, {'begin': '2020-03-06 14:00:20', 'end': '2024-08-13 23:59:50','record_id': 2,'name': 'RecordTwo'}]" -p -m=-1
```

### Параметры запуска

Обработка запуска через консоль реализована в `.\task_1\cli.py`.

`-records` | `-r`: JSON - строка с записями (__!Обязательное__)
`-add_months` | `-m`: Количество добавляемых месяцев. Принимает отрицательные значения (По умолчанию 0 - текущий месяц)
`-with_print` | `-p`: Флаг отвечающий за вывод записей в консоль (По умолчанию False)
`-include_dates` | `-p`: Флаг отвечающий за вывод дат в консоль (По умолчанию False)

> :warning: __`include_dates` применяется только с `with_print`__

### Настройки
Настройки находятся в файле `.\task_1\config.py`.

`RECORD_FORMAT_TEXT` = Шаблон для форматирования записей без дат
`DATE_FORMAT_TEXT` = Шаблон форматирования дат, добавляемый к `RECORD_FORMAT_TEXT`
`DATE_FORMAT` = Формат даты и времени в записях


### Тестирование
Юнит тесты находятся в `.\task_1\test\`

Для запуска тестов выполнить команду:
```
python -m unittest discover task_1
```


---

## Задание 2

Некоторая компания оказывает услуги физическим лицам. Каждая услуга имеет свой срок действия. В течение срока оказания услуги по ней могут предоставляться скидки.

Необходимо написать процедуру, которая собирает данные по оказанным услугам за месяц и их стоимость. На вход процедуры подается дата начала месяца (1-е число). В результате должна получится новая таблица, где будут собраны данные. Описание структур таблиц ниже.

```sql
CREATE TABLE `users` (
`user_id` int NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор пользователя',
`name` text COMMENT 'Имя пользователя',
`login` varchar(128) DEFAULT NULL COMMENT 'Логин пользователя',
`password` varchar(128) DEFAULT NULL COMMENT 'Пароль пользователя',
`contract_start_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Дата начала действия договора с пользователем',
`contract_expiration_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Дата окончания действия договора с пользователем',
PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='Пользователи';


CREATE TABLE `services` (
`service_id` int NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор услуги',
`user_id` int NOT NULL COMMENT 'Идентификатор пользователя',
`cost` decimal(20,6) NOT NULL DEFAULT '0.000000' COMMENT 'Стоимость услуги',
`name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Название услуги',
`timefrom` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'Дата начала оказания услуги',
`timeto` datetime NOT NULL DEFAULT '9999-12-31 23:59:59' COMMENT 'Дата завершения оказания услуги',
PRIMARY KEY (`service_id`),
KEY `user_id` (`user_id`),
CONSTRAINT `services_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES
`users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='Услуги, предоставляемые пользователю';

CREATE TABLE `discounts` (
`record_id` int NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор записи',
`name` varchar(64) DEFAULT NULL COMMENT 'Код скидки',
`service_id` int DEFAULT NULL COMMENT 'Идентификатор услуги',
`timefrom` datetime DEFAULT NULL COMMENT 'Начало действия скидки',
`timeto` datetime DEFAULT NULL COMMENT 'Окончание действия скидки',
`discount` decimal(20,6) DEFAULT NULL COMMENT 'Величина скидки в валюте',
PRIMARY KEY (`record_id`),
KEY `service_id` (`service_id`),
CONSTRAINT `discounts_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES
`services` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COMMENT='Скидки на услуги';
```

## Реализация - `.\task_2`

Файл - `task_2\get_monthly_service_report procedure.sql`
