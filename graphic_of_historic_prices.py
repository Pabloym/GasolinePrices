import matplotlib.pyplot as plt
import datetime
from constants import MAIN_PATH

# This script will be executed each day.

def load_data():
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
                galp_tuicides.append(float(line[1]))
                galp_viso.append(float(line[2]))
                galp_hermann.append(float(line[3]))
                carrefour.append(float(line[4]))
                bp.append(float(line[5]))
                petroprix.append(float(line[6]))
                try:
                    shell.append(float(line[7]))
                except:
                    pass
    return galp_tuicides, galp_viso, galp_hermann, carrefour, bp, petroprix, shell

def plot_line_chart():
    print("[INFO] Actualizando la gráfica de precios históricos...")

    galp_tuicides, galp_viso, galp_hermann, carrefour, bp, petroprix, shell = load_data()
    fig, ax = plt.subplots()

    ax.plot(galp_tuicides, "orange", marker='o', label="GALP - Tuicides")
    ax.plot(galp_viso, "c", marker='o', label="GALP - El Viso")
    ax.plot(galp_hermann, "black", marker='o', label="GALP - Hermann")
    ax.plot(bp, "g",  marker='o', label="BP")
    ax.plot(carrefour, "b",  marker='o', label="Carrefour")
    ax.plot(petroprix, "r",  marker='o', label="Petroprix")
    ax.plot(list(range(57, len(galp_viso))), shell, "fuchsia",  marker='o', label="Shell")

    plt.title('Histórico de precios')
    plt.xlabel('Días')
    plt.ylabel('Precios')
    plt.legend()
    plt.savefig("{}/Results/historic_prices.jpg".format(MAIN_PATH))
    plt.close()
    #plt.show()
    print("[INFO] Gráfica de precios históricos actualizada.")

