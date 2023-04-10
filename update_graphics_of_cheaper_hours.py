import matplotlib.pyplot as plt
from constants import MAIN_PATH


def load_data(name):
    galp = []
    with open("{}/Data/cheaper_hour_{}.csv".format(MAIN_PATH, name), "r") as csvfile:
        lines = csvfile.read().split("\n")
        for line in lines:
            if line and name not in line:
                line = line.split(",")
                galp.append([float(price) for price in line[1:]])

    return galp

def plot_line_chart_of_cheaper_hours(name: str):
    galp = load_data(name)
    headers = ["00.00","00.30","01.00","01.30","02.00","02.30","03.00","04.30","05.00","06.30","07.00","07.30","08.00","08.30","09.00","09.30","10.00","10.30","11.00","12.30","13.00","13.30","14.00","14.30","15.00","15.30","16.00","16.30","17.00","17.30","18.00","18.30","19.00","19.30","20.00","21.30","22.00","22.30","23.00","23.30"]

    fig, ax = plt.subplots()
    ax.plot(headers, galp[0], marker='o', label=f"GALP - {name.upper()}")
    for day in galp[1:]:
        ax.plot(headers, day, marker='o')

    plt.title('Prices during the last 30 days')
    plt.xlabel('Hours')
    plt.xticks(rotation=90)
    plt.ylabel('Prices')
    plt.legend()
    plt.savefig("{}/Results/cheaper_hour_{}.jpg".format(MAIN_PATH, name))
    plt.close()
    #plt.show()

