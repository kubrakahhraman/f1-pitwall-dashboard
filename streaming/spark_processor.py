import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp
from pyspark.sql.types import StructType, StructField, DoubleType, BooleanType
from elasticsearch import Elasticsearch, helpers

# Kafka bağlantı paketi
os.environ['PYSPARK_SUBMIT_ARGS'] = (
    '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 '
    'pyspark-shell'
)

# Elasticsearch bağlantı ayarları
ES_HOST = "localhost"
ES_PORT = 9200
ES_INDEX = "f1-telemetry-index"


def write_to_elasticsearch(batch_df, batch_id):
    """Her mikro-batch'i elasticsearch-py ile bulk olarak ES'e yazar."""
    rows = batch_df.collect()
    if not rows:
        print(f"Batch {batch_id}: boş, atlanıyor.")
        return

    es = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")

    actions = [
        {
            "_index": ES_INDEX,
            "_source": row.asDict()
        }
        for row in rows
    ]
    helpers.bulk(es, actions)
    print(f"Batch {batch_id}: {len(rows)} kayıt yazıldı, 0 hata.")


def main():
    # Spark oturumunu başlatıyoruz
    spark = SparkSession.builder \
        .appName("F1-Telemetry-Realtime-Processor") \
        .getOrCreate()

    # Terminalde çok fazla gereksiz log kalabalığı olmasın diye sadece uyarıları gösteriyoruz
    spark.sparkContext.setLogLevel("WARN")

    print("Spark başarıyla başlatıldı. Kafka dinleniyor...")

    # Kafka'dan canlı akışı okuma
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "f1-telemetry") \
        .option("failOnDataLoss", "false") \
        .load()

    # Hedef şemamız 
    telemetry_schema = StructType([
        StructField("RPM", DoubleType(), True),
        StructField("Speed", DoubleType(), True),
        StructField("Throttle", DoubleType(), True),
        StructField("nGear", DoubleType(), True),
        StructField("Brake", BooleanType(), True)
    ])

    # Kafka'dan gelen veriyi string'e ve ardından JSON şemasına çeviriyoruz
    parsed_df = df.select(
        from_json(col("value").cast("string"), telemetry_schema).alias("data")
    ).select("data.*")

    # @timestamp ekliyoruz ki anlık veri okunsun
    final_df = parsed_df.withColumn("@timestamp", current_timestamp())


    query = final_df.writeStream \
        .foreachBatch(write_to_elasticsearch) \
        .option("checkpointLocation", "es_checkpoint") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()