import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

database = pd.read_csv("D:\MOI\CentraleSupelec\Cours CS\Projet - Modélisation mathématiques\Test\Detection-de-fraudes\labelled_database.tsv", sep="\t")

base = database['income','taxclass']

print(base)

