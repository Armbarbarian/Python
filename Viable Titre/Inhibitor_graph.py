import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def graph():
    product1 = [0, 20, 40, 60, 80, 90, 100, 100, 100, 100]
    product2 = [0, 15, 30, 35, 45, 55, 65, 75, 85, 100]
    product3 = [0, 10, 20, 30, 35, 40, 45, 50, 50, 50]
    concentration_substrate = [*range(0, 100, 10)]

    plt.plot(concentration_substrate, product1, color='royalblue', marker='o', label='A')
    plt.plot(concentration_substrate, product2, color='firebrick', marker='o', label='B')
    plt.plot(concentration_substrate, product3, color='green', marker='o', label='C')

    plt.title('Substrate concentration against product formed')
    plt.xlabel('Substrate Concentration', fontsize=14)
    plt.ylabel('Product', fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=14)
    # plt.savefig('2021_enzymes_graph1.png')
    plt.show()


graph()
