import requests, json
from geopy import distance
from operator import itemgetter

# location = (44.9983525, 7.680287799999999)

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


def cerca_prezzo(location, carburante, distanza_max):
    """raw_data = (
        '{"points":[{"lat":'
        + str(location[0])
        + ',"lng":'
        + str(location[1])
        + '}],"fuelType":"'
        + carburante
        + '","priceOrder":"asc"}'
    )
    # raw_data = '{"points":[{"lat":44.9983525,"lng":7.680287799999999}],"fuelType":"1-1","priceOrder":"asc"}'
    r = requests.post(url=URL, data=raw_data, headers=HEADERS)
    data = (
        bytes(r.content.decode("utf-8"), "utf-8")
        .decode("unicode_escape")
        .replace("\\", "/")
    )"""
    f = open("data copy.json", "r")
    data = f.read()
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
                        "icon": "",
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
                            "icon": "",
                        }
                        validi.append(dati)
                        break
    validi = sorted(validi, key=itemgetter("distanza"))
    validi[0]["icon"] = "\U0001F680"
    validi = sorted(validi, key=itemgetter("prezzo"))

    """fw = open("valid.txt", "w")
    fw.write(str(validi))
    fw.close()
    """
    return validi