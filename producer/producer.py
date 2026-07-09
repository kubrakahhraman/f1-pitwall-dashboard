import os
import pandas as pd
import json
import time
import logging
import numpy as np
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def clean_for_json(d):
    """numpy tiplerini (int64, float64, NaN vs.) native Python tiplerine çevirir."""
    cleaned = {}
    for k, v in d.items():
        if isinstance(v, (np.integer,)):
            cleaned[k] = int(v)
        elif isinstance(v, (np.floating,)):
            cleaned[k] = None if np.isnan(v) else float(v)
        elif pd.isna(v):
            cleaned[k] = None
        else:
            cleaned[k] = v
    return cleaned


def get_producer():
    try:
        # Docker'da Kafka portuna bağlanıyoruz
        return KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            # Veriyi Kafka için JSON formatına çeviriyoruz
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    except Exception as e:
        logging.error(f"Kafka'ya bağlanılmadı! Docker çalışıyor mu? Hata: {e}")
        return None


def on_send_error(excp):
    logging.error(f"Mesaj gönderilemedi! Hata: {excp}")


def main():
    producer = get_producer()
    if not producer:
        return

    # Dosyanın doğru yere gitmesini sağlıyoruz
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '..', 'data', 'verstappen_telemetry.csv')

    try:
        logging.info("CSV dosyası açılıyor...")
        df = pd.read_csv(csv_path)

        logging.info("Veriler Kafka'ya yollanıyor!")

        # CSV'deki her bir satırı tek tek dönüyoruz, sanki o an araçtan geliyormuş gibi
        for index, row in df.iterrows():
            # Satırı sözlüğe çeviriyoruz ve numpy tiplerinden temizliyoruz
            data_dict = clean_for_json(row.to_dict())

            # 'f1-telemetry' isimli konuya veriyi gönderiyoruz, gönderim başarısız olursa haberimiz olsun

            producer.send('f1-telemetry', value=data_dict).add_errback(on_send_error)

            speed = data_dict.get('Speed', 'N/A')
            rpm = data_dict.get('RPM', 'N/A')
            gear = data_dict.get('nGear', 'N/A')
            logging.info(f"Yayında -> Vites: {gear} | RPM: {rpm} | Hız: {speed} km/h")

            # Gerçek zamanlı akış için sistemi 1 saniye bekletiyorum
            time.sleep(1)

    except FileNotFoundError:
        logging.error(f"CSV dosyası bulunamadı! Lütfen kontrol et: {csv_path}")
    except KeyboardInterrupt:
        logging.info("Canlı yayın manuel olarak durduruldu.")
    except Exception as e:
        logging.error(f"Beklenmeyen bir hata: {e}")
    finally:
        producer.flush()
        producer.close()
        logging.info("Sistem kapatıldı ve güvenle durdu.")

        


if __name__ == "__main__":
    main()