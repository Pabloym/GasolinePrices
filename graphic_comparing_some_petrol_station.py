import matplotlib.pyplot as plt
from constants import MAIN_PATH

def compute_galp_price(original_price):
    print("[INFO] Actualizando gŕafica comparando los precios de las estaciones de Galp Tucidides, Galp Hermann Hesse, Carrefour y Petropix.")

    # Estamos suponiendo que estamos echando gasolina del 1 al 5 de cada mes, donde Mapfre nos devuelve un 5%, sino sería un 3%.
    return original_price*0.95 - 0.1

def load_data():
    galp_tuicides = []
    galp_hermann = []
    carrefour = []
    petroprix = []
    with open("{}/Data/prices.csv".format(MAIN_PATH), "r") as csvfile:
        lines = csvfile.read().split("\n")
        for line in lines:
            if line and "Date" not in line:
                line = line.split(",")
                galp_tuicides.append(compute_galp_price(float(line[1])))
                galp_hermann.append(compute_galp_price(float(line[3])))
                # Con la tarjeta carrefour devuelve un 8% para compras en el carrefour
                carrefour.append(float(line[4])*0.92)
                petroprix.append(float(line[6]))
    return galp_tuicides[-30:], galp_hermann[-30:], carrefour[-30:], petroprix[-30:]

def plot_line_chart_of_comparisons():
    galp_tuicides, galp_hermann, carrefour, petroprix = load_data()
    fig, ax = plt.subplots()

    ax.plot(galp_hermann, "green", marker='o', label="GALP - Hermann")
    ax.plot(carrefour, "b",  marker='o', label="Carrefour")
    ax.plot(petroprix, "r",  marker='o', label="Petroprix")
    ax.plot(galp_tuicides, "orange", marker='o', label="GALP - Tuicides")


    plt.title('Precios de los últimos 30 días')
    plt.xlabel('Días')
    plt.ylabel('Precios')
    plt.legend()
    plt.savefig("{}/Results/comparison.jpg".format(MAIN_PATH))
    plt.close()
    #plt.show()

    print("[INFO] Gráfica comparando los precios de los últimos 30 días actualizada.")
