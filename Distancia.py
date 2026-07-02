import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "cd69edb1-9894-44cc-8b08-4c8dc4f9a594"      


def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data.get("message", "Ubicación no encontrada"))

    return json_status, lat, lng, new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en GraphHopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Elija un perfil de vehículo de la lista anterior (o 's' para salir): ")
    if vehicle == "s":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No se ingresó un perfil válido. Se usará el perfil 'car'.")

    loc1 = input("Ciudad de Origen (Chile): ")
    if loc1 == "s":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ciudad de Destino (Argentina): ")
    if loc2 == "s":
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print("Estado de la API de routing: " + str(paths_status) + "\nURL de la API de routing:\n" + paths_url)
        print("=================================================")
        print("Ruta desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
        print("=================================================")

        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            minutos = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, minutos, sec))
            print("=================================================")
            print("Narrativa del viaje:")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                texto = paths_data["paths"][0]["instructions"][each]["text"]
                distancia = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(texto, distancia / 1000, distancia / 1000 / 1.61))

            print("=================================================")
        else:
            print("Mensaje de error: " + paths_data.get("message", "No se pudo calcular la ruta"))
            print("*************************************************")
    else:
        print("No se pudo geocodificar el origen o el destino. Intente nuevamente.")

print("Programa finalizado. ¡Hasta luego!")