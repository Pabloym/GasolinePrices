import time
from datetime import datetime
import urllib
import csv
from tempfile import NamedTemporaryFile
import shutil
import requests
from update_graphics_of_cheaper_hours import plot_line_chart_of_cheaper_hours
from constants import MAIN_PATH

def download_data():
    ID_MUNICIPIO = 4521
    ID_PRODUCTO = 1
    URL = f"https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroMunicipioProducto/{ID_MUNICIPIO}/{ID_PRODUCTO}"

    urllib.request.urlretrieve(URL, "{}/Data/gasoline.txt".format(MAIN_PATH))

    print(("Donwloading data..."))

    file = open("{}/Data/gasoline.txt".format(MAIN_PATH), encoding="utf-8").read()
    #encoding="mcbs" if running on windows

    reintentos = 10
    while '"ListaEESSPrecio":[]' in file and reintentos > 0:
        print("[WARN] Los datos están vacios, descargando de nuevo...")
        time.sleep(60)
        urllib.request.urlretrieve(URL, "Data/gasoline.txt")
        file = open("{}/Data/gasoline.txt".format(MAIN_PATH), encoding="utf-8").read()
        reintentos -= 1

    list_of_prices = file.split("{")

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


def update_row_in_csv(hora, price, dia, filename, nombre):
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline="")
    
    row_template = {
        nombre: "", "00.00": "", "00.30": "", "01.00": "", "01.30": "", "02.00": "", "02.30": "", "03.00": "",
        "04.30": "", "05.00": "", "06.30": "", "07.00": "", "07.30": "", "08.00": "", "08.30": "", "09.00": "",
        "09.30": "", "10.00": "", "10.30": "", "11.00": "", "12.30": "", "13.00": "", "13.30": "", "14.00": "",
        "14.30": "", "15.00": "", "15.30": "", "16.00": "", "16.30": "", "17.00": "", "17.30": "", "18.00": "",
        "18.30": "", "19.00": "", "19.30": "", "20.00": "", "21.30": "", "22.00": "", "22.30": "", "23.00": "",
        "23.30": ""}    
    headers = list(row_template.keys())
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=headers)
        writer = csv.DictWriter(tempfile, fieldnames=headers)
        #writer.writeheader()

        for row in reader:
            if row[nombre] == dia:
                row[hora] = price
                writer.writerow(row)
            else:
                writer.writerow(row)
                
        if hora == "00.00" and int(datetime.today().minute) < 30:
            row = row_template
            row[nombre] = dia
            row[hora] = price
            writer.writerow(row)
            
    shutil.move(tempfile.name, filename)


def compute_cheaper_hour(rotulo, direccion, nombre):
    results, dia = download_data()
    precio = round(float([item['PrecioProducto'] for item in results if
                          (item['Rotulo'] == rotulo and item["Direccion"] == direccion)][0]), 3)

    hora = datetime.strftime(datetime.today(), "%H")
    minuto = "00" if int(datetime.today().minute) < 30 else "30"
    fecha = "{}.{}".format(hora, minuto)

    filename = "{}/Data/cheaper_hour_{}.csv".format(MAIN_PATH, nombre)

    if hora == "00" and int(datetime.today().minute) < 30:
        plot_line_chart_of_cheaper_hours("tucidides")
        plot_line_chart_of_cheaper_hours("herman_hesse")

    update_row_in_csv(fecha, precio, dia, filename, nombre)

compute_cheaper_hour(rotulo='GALP', direccion='CALLE TUICIDES', nombre='tucidides')
compute_cheaper_hour(rotulo='GALP', direccion='CALLE HERMAN HESSE', nombre='herman_hesse')
