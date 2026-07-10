# F1 Pitwall Dashboard - Real Time Telemetry Pipeline

![F1 Car](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3JuM3I0M3N6N29hbm0zM2FraGM3azBseWVyYWhvcWQ0bmw1anNlciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XCyZMXj9vL9xtMoVIN/giphy.gif)


> Gerçek zamanlı Formula 1 telemetri verilerini toplayan, işleyen, depolayan ve analiz eden; üzerine tahmin servisleri eklenebilen modüler bir veri platformu.


# Proje Hakkında

Formula 1 yarışları sırasında araçlardan saniyeler içinde binlerce telemetri verisi üretilmektedir. Bu veriler; hız, RPM, gaz pedalı, fren, vites, OM, SM, lastik bilgileri ve tur zamanları gibi birçok farklı metriği içerir.

Bu projenin amacı, Formula 1 telemetri verilerini gerçek zamanlı olarak işleyebilen modern bir veri mühendisliği platformu geliştirmektir.

Proje kapsamında;

- Telemetri verileri alınır.
- Gerçek zamanlı olarak işlenir.
- Temizlenir ve zenginleştirilir.
- Elasticsearch üzerinde indekslenir.
- Kibana üzerinden görselleştirilir.


# Projenin Amaçları

- Gerçek zamanlı veri işleme (Streaming)
- Veri mühendisliği mimarisi kurmak
- Ölçeklenebilir bir altyapı oluşturmak
- İleride eklenecek tahmin servisleri veya ML modellemesi için sağlam bir temel hazırlamaktır


# Sistem Mimarisi

```
                 FastF1 API
                      │
             Telemetry Producer
                      │
                 Apache Kafka
                      │
      Spark Structured Streaming
                      │
      DataParsing & Transformation
                      |           
                Elasticsearch         
                      │
              Kibana Dashboard
             
```

# Veri Akışı

```
FastF1 API

|

Telemetry Producer

|

Kafka

|

Spark Structured Streaming

|

Data Transformation

|

Elasticsearch

|

Kibana Dashboard

|

```

# Özellikler

- Gerçek zamanlı telemetri verisi işleme
- Apache Kafka ile veri akışı
- Spark Structured Streaming ile veri işleme
- PySpark ile Real-Time Data Transformation
- Elasticsearch indeksleme
- Kibana Dashboard


# Kullanılan Teknolojiler

| Programlama Dili : Python 
| Telemetri : FastF1 API
| Streaming : Apache Kafka 
| Veri İşleme : Apache Spark Structured Streaming
| Arama & Depolama : Elasticsearch
| Görselleştirme : Kibana 
| Containerization : Docker Compose


# Proje Yapısı

```
F1 Pitwall Dashboard - Real Time Telemetry Pipeline/

├── dashboard/            # Kibana dashboard ekran görüntüleri
├── data/                 # FastF1'den çekilen raw (ham) telemetri verileri
├── producer/             
│   └── producer.py       # Kafka'ya anlık veri basan data-generator kodu
├── streaming/            
│   └── spark_processor.py # PySpark gerçek zamanlı veri işleme (streaming) kodu
├── 1_fetch_data.py       # F1 API'den veriyi indirecek ana kod
├── docker-compose.yaml   # Kafka, Elasticsearch ve Kibana konteyner altyapısı
├── .gitignore            # Git'e yüklenmeyecek (venv, checkpoint vb.) dosyalar
├── requirements.txt      # Proje için gerekli Python kütüphaneleri
└── README.md             # Proje dokümantasyonu
```

# Nasıl çalışır

- Sanal Ortamı Hazırlayın:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows kullanıyorsanız: venv\Scripts\activate
   pip install -r requirements.txt


- İlk olarak verileri indirmek için şu komutu çalıştır:
   ```bash
   python 1_fetch_data.py

- Kafka ve Elasticsearch altyapısını ayağa kaldırmak için:
   ```bash
   docker-compose up -d

- Veri Akışını Başlatma: 
Producer ve Spark işlemcilerini çalıştırarak sistemi başlat:
   ```bash
   python producer/producer.py
   python streaming/spark_processor.py 

- Kibana arayüzüne gidiniz, veri akışını canlı olarak görebillirsiniz.

# Yol Haritası

## 1.0 (Tamamlandı)

- Telemetry Producer
- Kafka
- Spark Structured Streaming
- Elasticsearch
- Kibana Dashboard
- Docker Compose


## 1.1 (Planlananlar)

- Apache Airflow ile otomatik veri toplama
- Geçmiş yarışların arşivlenmesi
- ETL süreçlerinin zamanlanması


## 1.2 

- Kubernetes Deployment

## 2.0 

- Gap Prediction
- Battle Prediction
- Traffic Prediction
- Tyre Strategy Recommendation
- etc.


## 3.0

- Machine Learning Prediction Engine
- Tyre Degradation Prediction
- Lap Time Prediction
- Pit Strategy Recommendation

# Tasarım Kararları

Bu proje modüler olarak geliştirilmektedir.

İlk sürümde temel amaç gerçek zamanlı veri hattını oluşturmaktır.

Bu nedenle;

- Öncelik çalışan ve güvenilir bir streaming altyapısı kurmaktır.
- Docker Compose ile tüm servisler tek komutla ayağa kaldırılacaktır.
- Apache Airflow, yarış verilerinin otomatik toplanması amacıyla ileriki sürümlerde sisteme dahil edilecektir.
- Kubernetes, servisler container haline getirildikten sonra eklenecektir.
- Makine öğrenmesi modelleri ise veri platformu tamamen kararlı hale geldikten sonra geliştirilecektir.

Bu yaklaşım sayesinde platform adım adım büyütülebilecek ve her geliştirme aşaması bağımsız olarak test edilebilecektir.

# Dashboard

![Dashboard](https://s4.ezgif.com/tmp/ezgif-485506664ca79370.gif)



