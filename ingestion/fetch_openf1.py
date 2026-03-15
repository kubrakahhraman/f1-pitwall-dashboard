import requests
import json

BASE_URL = "https://api.openf1.org/v1"

def get_drivers(session_key="latest"):
      """OpenF1 API'den sürücü verisi çeker"""
      url = f"{BASE_URL}/drivers?session_key={session_key}"
      response = requests.get(url)
      return response.json()

def print_drivers(drivers):
      """Sürücü listesi ekrana yazdırır"""
      print("\n--- SÜRÜCÜ LİSTESİ ---")
      for driver in drivers:
            print(f"#{driver['driver_number']} {driver['full_name']} - {driver['team_name']}")

def save_drivers(drivers, filepath="ingestion/driver.json"):
      """Sürücü versini JSON dosyasına kaydeder"""
      with open(filepath, "w") as f:
            json.dump(drivers, f, indent=2)
      print(f"\nVeri {filepath} dosyasına kaydedildi!")

# Ana program
drivers = get_drivers()
print_drivers(drivers)
save_drivers(drivers)