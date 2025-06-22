from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date, month, lit
from pyspark.sql.types import IntegerType, DecimalType, StringType, BooleanType
from pyspark.sql.utils import AnalysisException

spark = SparkSession.builder.appName("Parquet transformation with logging to S3").getOrCreate()

source_path = "s3a://s3-etl-final/transactions_v2.csv"
target_path = "s3a://s3-etl-final-transformed-data/transactions_v2_transformed.parquet"

try:
    print(f"Чтение данных из: {source_path}")
    df = spark.read.option("header", "true").csv(source_path)
    
    print("Схема исходных данных:")
    df.printSchema()
    
    # Приведение типов + формат даты YYYYMMDD
    df = df.withColumn("msno", col("msno").cast(StringType())) \
           .withColumn("actual_amount_paid", col("actual_amount_paid").cast(DecimalType(10,2))) \
           .withColumn("plan_list_price", col("plan_list_price").cast(DecimalType(10,2))) \
           .withColumn("is_auto_renew", col("is_auto_renew").cast(BooleanType())) \
           .withColumn("is_cancel", col("is_cancel").cast(BooleanType())) \
           .withColumn("membership_expire_date", to_date(col("membership_expire_date").cast("string"), "yyyyMMdd")) \
           .withColumn("transaction_date", to_date(col("transaction_date").cast("string"), "yyyyMMdd")) \
           .withColumn("payment_method_id", col("payment_method_id").cast(IntegerType())) \
           .withColumn("payment_plan_days", col("payment_plan_days").cast(IntegerType()))
    
    print("Схема преобразованных данных:")
    df.printSchema()

    # Удаляем строки с пропущенными обязательными полями
    df = df.na.drop(subset=["msno", "transaction_date"])
    
    # Заполняем поля значениями по умолчанию
    df = df.fillna({"actual_amount_paid": 0.0,  "is_cancel": False, "is_auto_renew": False})
    
    # Фильтруем файл по дате транзакции
    df = df.where(col("transaction_date") > to_date(lit('2017-01-01')))  
    
    # Создаем новое поле для разделения датасета на разные файлы
    df = df.withColumn("month", month(col("transaction_date")))
    
    print(f"Запись в Parquet: {target_path}")
    df.repartition(1, "month").write.partitionBy("month").mode("overwrite").parquet(target_path)
    
    
    print("Данные успешно преобразованы и сохранены в Parquet")

except AnalysisException as ae:
    print("Ошибка анализа:", ae)
except Exception as e:
    print("Общая ошибка:", e)

finally:
    spark.stop()  