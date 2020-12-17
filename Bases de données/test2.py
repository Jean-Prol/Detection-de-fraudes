import pandas as pd
from sodapy import Socrata
import pickle
import random 
import matplotlib.pyplot as plt

"""
Unauthenticated client only works with public data sets. Note 'None'
in place of application token, and no username or password:
"""
##client = Socrata("data.cityofnewyork.us", None)

"""
Example authenticated client (needed for non-public datasets):
client = Socrata(data.cityofnewyork.us,
              MyAppToken,
              userame="user@example.com",
            password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
"""

##results = client.get("yjxr-fw8i", limit=2000)

"""
Convert to pandas DataFrame
"""

##results_df = pd.DataFrame.from_records(results)
##results_df.to_csv(r"/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Bases de données/Property.csv")

L = [0.017053212, 0.026934656, 0.10808975, 0.151695514, 0.197039152, 0.154728978, 0.068953478, 0.11005991, 0.16544535]
K = [round(2000*elem) for elem in L]
M = [1, 10000, 15000, 25000, 35000, 50000, 65000, 75000, 100000, 1000000]
I = []

for i in range(len(L)):
    for _ in range(K[i]):
        I.append(random.randrange(M[i], M[i+1]))

#print(I)
#print(len(I))

with open('/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Bases de données/Incomes.pkl', 'rb') as f:
    data = pickle.load(f)

data_df = pd.DataFrame.from_records(data).T

stock = data_df.dropna(subset=["total_stock_value"])["total_stock_value"]

P = stock.values.tolist()
Q = [elem for elem in P if type(elem)==int]


A = [-100000, 0, 500000, 1000000, 2000000, 3000000, 4000000, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000, 35000000, 40000000, 50000000, 400000000]
B = [0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0]

for elem in Q:
    i=0
    while i<16 and elem>A[i]:
        i+=1
    B[i-1]+=1

C = [elem/126 for elem in B]

D = [round(2000*elem) for elem in C]
J = []

for i in range(len(D)):
    for _ in range(D[i]):
        J.append(random.randrange(A[i], A[i+1]))

print(J)
