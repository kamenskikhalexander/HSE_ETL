import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_json, struct, rand


SOURCE = "s3a://s3-etl-final-transformed-data/transactions_v2_transformed.parquet/month=1/part-00000-fea6f67b-3dbd-4a82-8e13-8f5194f24d57.c000.snappy.parquet"


def main():
    spark = SparkSession.builder.appName("write-to-kafka").getOrCreate()
    
    try:
        df = spark.read.parquet(SOURCE)
        
        while True:
            batch_df = df.orderBy(rand()).limit(100)
            
            # Преобразуем в JSON 
            kafka_df = batch_df.select(to_json(struct([col(c) for c in batch_df.columns])).alias("value"))
            
            # Записываем батч в Kafka
            kafka_df.write.format("kafka") \
                .option("kafka.bootstrap.servers", "rc1d-8iaqdsnnav7ufl0q.mdb.yandexcloud.net:9091") \
                .option("topic", "kafka-topic-etl-final") \
                .option("kafka.security.protocol", "SASL_SSL") \
                .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
                .option("kafka.sasl.jaas.config",
                       "org.apache.kafka.common.security.scram.ScramLoginModule required "
                       "username='user1' "
                       "password='password1';") \
                .save()
            
            time.sleep(0.5)
            
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()


