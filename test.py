import requests

# Twój link do pliku GPX
url = "https://api.sports-tracker.com/apiserver/v1/workout/exportGpx/686d440bd697897cea806bfd?token=7soo2brfbum19pdoncjnma8b64681kfb"

# Wysłanie żądania GET
response = requests.get(url)

# Sprawdzenie statusu i zapis do pliku
if response.status_code == 200:
    with open("trening.gpx", "wb") as f:
        f.write(response.content)
    print("Plik GPX został pobrany jako 'trening.gpx'")
else:
    print(f"Błąd pobierania: {response.status_code}")
