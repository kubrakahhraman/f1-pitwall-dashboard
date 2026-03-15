import requests
import json

BASE_URL = "https://api.openf1.org/v1"

def get_pit_stops(session_key="latest"):
    """OpenF1 API'den pit stop verilerini çeker"""
    url = f"{BASE_URL}/pit?session_key={session_key}"
    response = requests.get(url)
    return response.json()

def print_pit_stops(pit_stops):
    """Pit stop listesini ekrana yazdırır"""
    print("\n--- PIT STOP LİSTESİ ---")
    for pit in pit_stops:
        print(f"Sürücü #{pit['driver_number']:<3} - Tur {pit['lap_number']:<3} - Süre: {pit['pit_duration']}sn")

# Ana program
pit_stops = get_pit_stops()
print_pit_stops(pit_stops)

