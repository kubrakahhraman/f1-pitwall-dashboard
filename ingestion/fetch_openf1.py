import requests
import json

# OpenF1 API'den veri çek
url = "https://api.openf1.org/v1/drivers?session_key=latest"

response = requests.get(url)

print("Durum kodu:", response.status_code)
# print("Toplam sürücü sayısı:", len(response.json()))

# for driver in response.json():
#       print(driver['full_name'], "-", driver["team_name"])

# print("İlk sürücü:", response.json()[0])

# Veriyi düzenli göster
print("\n--- SÜRÜCÜ LİSTESİ ---")
for driver in response.json():
      print(f"{driver["driver_number"]:3} | {driver["full_name"]:25} | {driver["team_name"]}")
