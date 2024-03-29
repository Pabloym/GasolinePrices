import datetime
import numpy as np
import pandas as pd
from constants import MAIN_PATH

# This script have to be executed weekly on Sunday.


def date_to_weekday(date):
    d, m, y = date.split("/")
    return datetime.datetime(int(y), int(m), int(d)).weekday()


today = datetime.date.today().strftime("%d/%m/20%y")

#if date_to_weekday(today) != 6:
#    raise Exception("The results must be update only on Sunday.")

def get_data():
    galp_tuicides = []
    galp_viso = []
    galp_hermann = []
    carrefour = []
    bp = []
    petroprix = []
    shell = []

    with open("{}/Data/prices.csv".format(MAIN_PATH), "r") as csvfile:
        lines = csvfile.read().split("\n")
        for line in lines:
            if line and "Date" not in line:
                line = line.split(",")
                galp_tuicides.append((line[0], line[1]))
                galp_viso.append((line[0], line[2]))
                galp_hermann.append((line[0], line[3]))
                carrefour.append((line[0], line[4]))
                bp.append((line[0], line[5]))
                petroprix.append((line[0], line[6]))
                try:
                    shell.append((line[0], line[7]))
                except:
                    pass
    return galp_tuicides, galp_viso, galp_hermann, carrefour, bp, petroprix, shell

def cheaper_day(petrol_station):
    """
    Function useful to get the weekday when the petrol is cheaper.
    It only will be executed on Sundays, when the prices of all the week are available.

    If the lowest price appears several times, it will return a list with all of these days.
    """
    prices = [price for date, price in petrol_station][-7:]
    index_of_lower_price = np.argmin(prices)
    minimun = prices[index_of_lower_price]
    indexes = [index for index in range(len(prices)) if prices[index] == minimun]
    isMinimunRepeated = len(indexes) > 1
    if isMinimunRepeated:
        return indexes
    return [index_of_lower_price]


def update_csv_data(petrol_station, petrol_station_name):
    path = "{}/Data/cheaper_day_for_{}.csv".format(MAIN_PATH, petrol_station_name)
    df = pd.read_csv(path)
    dict_of_weekday = {0: "Lunes", 1: "Martes", 2: "Miercoles", 3: "Jueves", 4: "Viernes", 5: "Sabado", 6: "Domingo"}
    weekdays = [dict_of_weekday[day] for day in cheaper_day(petrol_station)]
    for weekday in weekdays:
        value_to_update = df._get_value(0, weekday)
        df[weekday] = df[weekday].replace({value_to_update: value_to_update + 1})
    df.to_csv(path, index=False)
    print(f"[DEBUG] Estadásticas de {petrol_station_name} actualizada.")


def update_csv():
    galp_tuicides, galp_viso, galp_hermann, carrefour, bp, petroprix, shell = get_data()

    update_csv_data(galp_tuicides, "galp_tuicides")
    update_csv_data(galp_viso, "galp_el_viso")
    update_csv_data(galp_viso, "galp_hermann")
    update_csv_data(carrefour, "carrefour")
    update_csv_data(petroprix, "petroprix_licurgo")
    update_csv_data(bp, "bp_camino_suarez")
    update_csv_data(shell, "shell")

    print("[INFO] Datos de cada estación actualizados.")
