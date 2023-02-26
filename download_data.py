from datetime import datetime
import urllib
import requests
import csv
import numpy as np

# This script has to be executed each day.
from emails import send_emails
from graphic_comparing_some_petrol_station import plot_line_chart_of_comparisons
from graphic_of_historic_prices import plot_line_chart
from make_graphics import make_graphic_for_cheaper_day
from update_csv import update_csv


def download_data():
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

    return results, date


def recover_data(petrol_station):
    with open("Data/prices.csv", "r") as csvfile:
        lines = csvfile.read().split("\n")
        header = lines[0].split(",")
        last_record = lines[-1]
        i = 1
        while not last_record:
            i += 1
            last_record = lines[-i]

        last_record = last_record.split(",")

        records = {}
        for j in range(0, len(header) - 1):
            records[header[j]] = last_record[j]

        return records[petrol_station]


def polish_data(results, date):
    filtering_petrol_station = [("CALLE ESTEBAN SALAZAR CHAPELA", "SHELL", "SHELL"), ("CALLE TUICIDES", "GALP", "GALP-TUICIDES"), ("AVENIDA AVDA. WASHINGTON-POLIG. EL VISO", "GALP", "GALP-EL VISO"), ("CALLE HERMAN HESSE", "GALP", "GALP-HERMANN"), ("CALLE SAIN EXUPERY", "CARREFOUR", "CARREFOUR"), ("AV VALLE INCLAN", "BP CAMINO SUAREZ", "BP CAMINO SUAREZ"), ("CALLE LICURGO", "PETROPRIX", "PETROPRIX-LICURGO")]

    final_results = dict()
    final_results["Date"] = date

    for street, petrol_station, label in filtering_petrol_station:
        for data in results:
            if data["Direccion"] == street and data["Rotulo"] == petrol_station:
                new_data = data["PrecioProducto"]
                if new_data:
                    final_results[label] = new_data
                else:
                    print(f"[INFO] Getting data from the last record in {recover_data('Date')} for {label}.")
                    final_results[label] = recover_data(label)
    return final_results

def write_new_record(record):
    headers = ["Date", "GALP-TUICIDES", "GALP-EL VISO", "GALP-HERMANN", "CARREFOUR", "BP CAMINO SUAREZ", "PETROPRIX-LICURGO", "SHELL"]

    with open("Data/prices.csv", "a", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        #writer.writeheader()
        writer.writerow(record)
        csvfile.close()

    print(f"[INFO] Data updated to the current date {record['Date']}.")


def get_indexs_with_minimun_price(prices):
    minimo = min(prices)
    return [index for index in [0,1,2,3,4,5,6] if prices[index] == minimo]


def compute_statistics_for_last_week():
    galp_tuicides = []
    with open("Data/prices.csv", "r") as csvfile:
        lines = csvfile.read().split("\n")
        for line in lines:
            if line and "Date" not in line:
                line = line.split(",")
                galp_tuicides.append(float(line[1]))

    number_of_days = 7
    prices = galp_tuicides[-number_of_days:]

    precio_min = min(prices)
    precio_max = max(prices)
    precio_medio = round(sum(prices)/float(number_of_days), 3)

    dict_of_weekday = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves", 4: "Viernes", 5: "Sabado", 6: "Domingo"}

    days = [dict_of_weekday[int(day)] for day in get_indexs_with_minimun_price(prices)]
    return precio_medio, precio_min, precio_max, ", ".join(days)


def main_donwload_data():
    results, date = download_data()
    final_results = polish_data(results, date)
    write_new_record(final_results)

    plot_line_chart()

    if datetime.today().weekday() == 6:
        print("[INFO] Updating the cheaper weekday.")
        update_csv()
        make_graphic_for_cheaper_day()

        plot_line_chart_of_comparisons()
        precio_medio, precio_min, precio_max, dias = compute_statistics_for_last_week()
        send_emails(precio_medio, precio_min, precio_max, dias)


main_donwload_data()
