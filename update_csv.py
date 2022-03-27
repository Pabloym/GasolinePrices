import datetime
import numpy as np
import pandas as pd

# This script have to be executed weekly on Sunday.

galp_tuicides = []
galp_viso = []
carrefour = []
bp = []
petroprix = []


def date_to_weekday(date):
    d, m, y = date.split("/")
    return datetime.datetime(int(y), int(m), int(d)).weekday()


today = datetime.date.today().strftime("%d/%m/20%y")

if date_to_weekday(today) != 6:
    raise Exception("The results must be update only on Sunday.")

with open("Data/prices.csv", "r") as csvfile:
    lines = csvfile.read().split("\n")
    for line in lines:
        if line and "Date" not in line:
            line = line.split(",")
            galp_tuicides.append((line[0], line[1]))
            galp_viso.append((line[0], line[2]))
            carrefour.append((line[0], line[3]))
            bp.append((line[0], line[4]))
            petroprix.append((line[0], line[5]))


def cheaper_day(petrol_station):
    """
    Function useful to get the weekday when the petrol is cheaper.
    It only will be executed on Sundays, when the prices of all the week are available.
    """
    prices = [price for date, price in petrol_station][-7:]
    return np.argmin(prices)


def update_csv_data(petrol_station, petrol_station_name):
    path = f"Data/cheaper_day_for_{petrol_station_name}.csv"
    df = pd.read_csv(path)
    dict_of_weekday = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    weekday = dict_of_weekday[cheaper_day(petrol_station)]
    value_to_update = df._get_value(0, weekday)
    df[weekday] = df[weekday].replace({value_to_update: value_to_update + 1})
    df.to_csv(path, index=False)
    print(f"Update completed for petrol station: {petrol_station_name}")


update_csv_data(galp_tuicides, "galp_tuicides")
update_csv_data(galp_viso, "galp_el_viso")
update_csv_data(carrefour, "carrefour")
update_csv_data(petroprix, "petroprix_licurgo")
update_csv_data(bp, "bp_camino_suarez")
