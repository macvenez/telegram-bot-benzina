import requests, json
from geopy import distance
from operator import itemgetter

location = (44.9983525, 7.680287799999999)
distanza_max = 5
"""
URL = "https://carburanti.mise.gov.it/ospzApi/search/zone"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://carburanti.mise.gov.it",
    "Connection": "keep-alive",
    "Referer": "https://carburanti.mise.gov.it/ospzSearch/zona",
    "Cookie": "cookies_consent=true",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

raw_data = '{"points":[{"lat":44.9983525,"lng":7.680287799999999}],"fuelType":"1-1","priceOrder":"asc"}'
r = requests.post(url=URL, data=raw_data, headers=HEADERS)
# data = str(r.content)
data = (
    bytes(r.content.decode("utf-8"), "utf-8")
    .decode("unicode_escape")
    .replace("\\", "/")
)
f = open("data.json", "w")
f.write(data)
f.close()
"""


def cerca_prezzo(location, distanza_max):
    with open("data copy.json", "r") as file:
        data = json.load(file)["results"]
        # filedata = file.read()
    validi = []

    for benzinaio in data:
        distanza = distance.distance(
            [benzinaio["location"].get("lat"), benzinaio["location"].get("lng")],
            location,
        ).km
        if distanza <= distanza_max:
            for benzina in benzinaio["fuels"]:
                if benzina.get("fuelId") == 1 and benzina.get("isSelf") == True:
                    break
            dati = {
                "id": benzinaio["id"],
                "distanza": distanza,
                "nome": benzinaio["name"],
                "prezzo": benzina["price"],
                "luogo": benzinaio["address"],
                "marca": benzinaio["brand"],
                "coord": benzinaio["location"],
            }
            validi.append(dati)
    validi = sorted(validi, key=itemgetter("prezzo"))
    fw = open("valid.txt", "w")
    fw.write(str(validi))
    fw.close()
    return validi
