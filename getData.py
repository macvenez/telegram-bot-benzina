import requests, json
from operator import itemgetter
from geopy import distance
from datetime import datetime

import _secret

testing = 0  # set this to 0 if you want to request data from the internet instead from file (used to reduce api requests)


def cerca_prezzo(location, carburante, distanza_max):
    if testing == 0:
        json_data = {
            "points": [
                {
                    "lat": str(location[0]),
                    "lng": str(location[1]),
                },
            ],
            "fuelType": "1-1",
            "priceOrder": "asc",
            "radius": distanza_max,
        }
        # r = requests.post(url=_secret.URL, data=raw_data, headers=_secret.HEADERS)
        r = requests.post(
            _secret.URL,
            headers=_secret.HEADERS,
            json=json_data,
        )
        data = (
            bytes(r.content.decode("utf-8"), "utf-8")
            .decode("unicode_escape")
            .replace("\\", "/")
        )
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + " --> getData.py --> Requested data from internet")
    else:
        f = open("data copy.json", "r")
        data = f.read()
        f.close()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + " --> getData.py --> Requested data from file")

    data = json.loads(data)["results"]
    validi = []
    for benzinaio in data:
        distanza = distance.distance(
            [benzinaio["location"].get("lat"), benzinaio["location"].get("lng")],
            location,
        ).km
        if distanza <= distanza_max:
            for benzina in benzinaio["fuels"]:
                if int(benzina.get("fuelId")) == int(carburante[0]):
                    dati = {
                        "id": benzinaio["id"],
                        "distanza": distanza,
                        "nome": benzinaio["name"],
                        "prezzo": benzina["price"],
                        "luogo": benzinaio["address"],
                        "marca": benzinaio["brand"],
                        "coord": benzinaio["location"],
                        "dist": distanza,
                    }
                    validi.append(dati)
                    break
                if carburante[0] == "1" or carburante[0] == "2":
                    if benzina.get("isSelf") == True and int(
                        benzina.get("fuelId")
                    ) == int(carburante[0]):
                        dati = {
                            "id": benzinaio["id"],
                            "distanza": distanza,
                            "nome": benzinaio["name"],
                            "prezzo": benzina["price"],
                            "luogo": benzinaio["address"],
                            "marca": benzinaio["brand"],
                            "coord": benzinaio["location"],
                            "dist": distanza,
                        }
                        validi.append(dati)
                        break
    validi = sorted(validi, key=itemgetter("prezzo"))
    return validi
