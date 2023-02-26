import matplotlib.pyplot as plt

# This script will be executed each day.
print("[INFO] Updating the graphic of the comparison between Galp Tucidides, Galp Hernan Hesse, Carrefour and Petropix prices.")

def compute_galp_price(original_price):
    # Estamos suponiendo que estamos echando gasolina del 1 al 5 de cada mes donde Mapfre nos devuelve un 5%.
    return original_price*0.95 - 0.1

def load_data():
    galp_tuicides = []
    galp_hermann = []
    carrefour = []
    petroprix = []
    with open("Data/prices.csv", "r") as csvfile:
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


    plt.title('Prices during the last 30 days')
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.legend()
    plt.savefig("Results/comparison.jpg")
    plt.close()
    #plt.show()

plot_line_chart_of_comparisons()

print("[INFO] Graphic of the comparison updated.")
