pwd

quit
close
ls
exit
exit heredoc
# F1 Telemetry Data Engineering Project

## Proje Amacı
Formula 1 yarış verilerini toplayıp işleyen uçtan uca bir veri mühendisliği pipeline'ı oluşturmak.

## Mimari
FastF1/OpenF1 API -> Python -> PostgreSQL -> Airflow -> Spark -> S3/MinIO -> Plotly/Kibana

## Klasör Yapısı
- ingestion/      → Veri toplama scriptleri
- transformation/ → Spark ile veri işleme
- orchestration/  → Airflow DAG'ları
- storage/        → Veritabanı şemaları
- notebooks/      → Analiz ve ML
- docs/           → Dokümantasyon
