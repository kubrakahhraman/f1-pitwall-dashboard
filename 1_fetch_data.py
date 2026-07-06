import fastf1
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
      # Ortamı hazırlıyoruz
      os.makedirs('./data/cache', exist_ok=True)
      fastf1.Cache.enable_cache('./data/cache')
      logging.info("Ortam hazır, F1 API bağlanıyor...")

      # Veriyi çekme
      session = fastf1.get_session(2026, 'Austria', 'R')
      session.load()

      verstappen = session.laps.pick_driver('3')
      telemetry = verstappen.get_telemetry()

      # Veri kaybını engellemek için yedekleme
      csv_path = 'data/verstappen_telemetry.csv'
      telemetry.to_csv(csv_path, index=False)
      logging.info(f"Başarılı! Veri güvende: {csv_path}")

except Exception as e:
      # Eğer veri çekilirken sorun olursa, sorunlar buraya düşer ve nerede sorun olduğunu söyler.
      logging.error(f"Hata! Veri çekilemedi: {e}")
