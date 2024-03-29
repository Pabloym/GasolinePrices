import matplotlib.pyplot as plt
import datetime
from constants import MAIN_PATH


# This script will be executed each Sunday.

def date_to_weekday(date):
    d, m, y = date.split("/")
    return datetime.datetime(int(y), int(m), int(d)).weekday()


def statistics_of_the_cheaper_day_of_a_week(name):
    with open("{}/Data/cheaper_day_for_{}.csv".format(MAIN_PATH, name), "r") as csvfile:
        lines = csvfile.read().split("\n")
        days = lines[0].split(",")
        statistics = [int(value) for value in lines[1].split(",")]

    y_pos = [1, 2, 3, 4, 5, 6, 7]
    plt.bar(y_pos, statistics)
    plt.xticks(y_pos, days, rotation=15)
    plt.title('Días más baratos de la semana')
    plt.savefig("{}/Results/cheaper_day_{}".format(MAIN_PATH, name))
    plt.close()
    #plt.show()

def make_graphic_for_cheaper_day():
    statistics_of_the_cheaper_day_of_a_week("galp_tuicides")
    statistics_of_the_cheaper_day_of_a_week("galp_el_viso")
    statistics_of_the_cheaper_day_of_a_week("galp_hermann")
    statistics_of_the_cheaper_day_of_a_week("carrefour")
    statistics_of_the_cheaper_day_of_a_week("petroprix_licurgo")
    statistics_of_the_cheaper_day_of_a_week("bp_camino_suarez")
    statistics_of_the_cheaper_day_of_a_week("shell")

    print("Gráficos con las estadísticas de cada estación actualizadas.")
