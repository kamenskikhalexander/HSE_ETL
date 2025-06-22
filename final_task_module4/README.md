# Итоговое задание ETL

### Этапы проекта:
- Создание базы данных в Yandex Database (YDB) и настройка репликации в Yandex Object Storage (S3);
- Развертывание и конфигурация Managed Service for Apache Airflow, вместе с Yandex MetaDataHub;
- Разработка PySpark-скриптов и создание DAG для автоматизации процессов обработки данных;
- Развертывания и конфигурация Apache Kafka в Managed Service for Apache Kafka;
- Создание PySpark-скриптов реализующих kafka-producer и kafka-consumer;
- Визуализация обработанных данных с использованием Yandex DataLens и Yandex Query.

В рамках работы был использован датасет transactions_v2 с [kaggle](https://www.kaggle.com/datasets), содержащий данные о платежах за подписку.

### Задание 1. Работа с Yandex DataTransfer
- Развернута YDB и создана таблица для датасета transactions_v2
![Создана YDB](https://github.com/user-attachments/assets/06c574a1-3b6a-4173-b299-c72cf78c0c2d)
#### Скрипт создания таблицы в YDB
```    
CREATE TABLE transactions_v2(
    msno String,
    payment_method_id Int32,
    payment_plan_days Int32,
    plan_list_price Int32,
    actual_amount_paid Int32,
    is_auto_renew Int8,
    transaction_date Utf8,
    membership_expire_date Utf8,
    is_cancel Int8,
    PRIMARY KEY (msno),
    INDEX `idx_transaction_date` GLOBAL ASYNC  ON (`transaction_date`),
    INDEX `idx_payment_method_id` GLOBAL ASYNC ON (`payment_method_id`) ,
    INDEX `idx_is_cancel` GLOBAL ASYNC ON (`is_cancel`)
);
```
*Также были созданы индексы по ключевым полям поиска.
- В созданную таблицу с помощью CLI загружен датасет transaction_v2

#### bash скрипт
```  
ydb -p quickstart import file csv -p transactions_v2 --header --null-value "" transactions_v2.csv
```
*Параметр quickstart - использование ранее созданного профиля в Yandex CLI
![Загружен датасет в YDB](https://github.com/user-attachments/assets/0214e1a6-23d8-4ba0-ac8f-09695394f622)
- Создан трансфер данных в Yandex Data Transfer  с эндпоинтом-источником в YDB и эндпоинтом-приемником в Object Storage для репликации данных между ними. Формат файл изменен на .parquet для дальнейщего хранения и работы `s3a://s3-etl-final/transactions_v2.parquet`

Дата трансфер:
![Дата трансфер создан](https://github.com/user-attachments/assets/956e93d7-4ca2-4061-bd5e-72eaaa7d6bff)
Загрузка в бакет:
![Файл загружен в бакет](https://github.com/user-attachments/assets/603cc051-859d-4340-b156-13c63bff164b)




