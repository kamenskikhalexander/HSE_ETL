from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    spark = SparkSession.builder.appName("read-messages-from-kafka").getOrCreate()

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "rc1d-8iaqdsnnav7ufl0q.mdb.yandexcloud.net:9091") \
        .option("subscribe", "kafka-topic-etl-final") \
        .option("kafka.security.protocol", "SASL_SSL") \
        .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
        .option("kafka.sasl.jaas.config",
                "org.apache.kafka.common.security.scram.ScramLoginModule required "
                "username='user1' "
                "password='password1';") \
        .option("startingOffsets", "earliest") \
        .load()

    final_df = kafka_df.selectExpr("CAST(value AS STRING)").where(col("value").isNotNull())

    # Сохраняем поток JSON в S3
    query = final_df.writeStream \
        .format("json") \
        .option("path", "s3a://dataproc-bucket-hse/kafka-read-stream-output") \
        .option("checkpointLocation", "s3a://dataproc-bucket-hse/checkpoints/kafka-json") \
        .trigger(once=True) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
