import urllib
import requests
import csv

# This script has to be executed each day.

ID_MUNICIPIO = 4521
ID_PRODUCTO = 1
URL = f"https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroMunicipioProducto/{ID_MUNICIPIO}/{ID_PRODUCTO}"

urllib.request.urlretrieve(URL, "Data/gasoline.txt")

print(("Donwloading data..."))

file = open("Data/gasoline.txt", encoding="utf-8")
#encoding="mcbs" if running on windows

list_of_prices = file.read().split("{")

date = list_of_prices[1].split("\"")[3].replace("\\", "").split(" ")[0]

results = []

for x in list_of_prices[2:]:
    data = x.replace("\"", "")\
            .replace("},", "")\
            .replace("\\", "")\
            .replace("Ã³", "o")\
            .replace("Ã¡","a")\
            .replace("","")\
            .replace("ó","o")\
            .replace("Ã","A")\
            .split("}],")[0]\
            .split(",")
    dictionary = {}
    for i in range(len(data)):
        item = data[i]
        if "PrecioProducto" in item:
            item = ".".join([item, data[i+1]])
        key_value = item.split(":")
        key = key_value[0]
        if len(key_value) > 1:
            value = "".join(key_value[1:])
        if key == "Direccion" or key == "Rotulo":
            dictionary[key] = value
        elif key == "PrecioProducto":
            dictionary[key] = float(value)
    if dictionary:
        results.append(dictionary)

filtering_petrol_station = [("CALLE TUICIDES", "GALP", "GALP-TUICIDES"), ("AVENIDA AVDA. WASHINGTON-POLIG. EL VISO", "GALP", "GALP-EL VISO"), ("CALLE HERMAN HESSE", "GALP", "GALP-HERMANN"), ("CALLE SAIN EXUPERY", "CARREFOUR", "CARREFOUR"), ("AV VALLE INCLAN", "BP CAMINO SUAREZ", "BP CAMINO SUAREZ"), ("CALLE LICURGO", "PETROPRIX", "PETROPRIX-LICURGO")]

final_results = dict()
final_results["Date"] = date

for street, petrol_station, label in filtering_petrol_station:
    for data in results:
        if data["Direccion"] == street and data["Rotulo"] == petrol_station:
            final_results[label] = data["PrecioProducto"]

headers = ["Date", "GALP-TUICIDES", "GALP-EL VISO", "GALP-HERMANN", "CARREFOUR", "BP CAMINO SUAREZ", "PETROPRIX-LICURGO"]

with open("Data/prices.csv", "a") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    #writer.writeheader()
    writer.writerow(final_results)
    csvfile.close()

print(f"Data updated to the current date {date}.")
