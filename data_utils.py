import pandas as pd
from sodapy import Socrata
import pickle
import random

with open('Incomes.pkl', 'rb') as f:
    data = pickle.load(f) 

def property_data(n) :
    
    client = Socrata("data.cityofnewyork.us", None)
    results = client.get("yjxr-fw8i", limit=n)
    results_df = pd.DataFrame.from_records(results)
    return(results_df)

def income_data(n) :

    L = [0.017053212, 0.026934656, 0.10808975, 0.151695514, 0.197039152, 0.154728978, 0.068953478, 0.11005991, 0.16544535]
    K = [round(n*elem) for elem in L]
    M = [1, 10000, 15000, 25000, 35000, 50000, 65000, 75000, 100000, 1000000]
    income = []

    for i in range(len(L)):
        for _ in range(K[i]):
            income.append(random.randrange(M[i], M[i+1]))
    return income




def deferred_income_data(n) :
    A = [-100000, 0, 500000, 1000000, 2000000, 3000000, 4000000, 5000000, 10000000, 15000000, 20000000, 25000000, 30000000, 35000000, 40000000, 50000000, 400000000]
    B = [0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0]
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    stock = data_df.dropna(subset=["total_stock_value"])["total_stock_value"]
    P = stock.values.tolist()
    for elem in P:
        i=0
        while i<16 and elem>A[i]:
            i+=1
            B[i-1]+=1

    C = [elem/126 for elem in B]

    D = [round(n*elem) for elem in C]
    J = []

    for i in range(len(D)):
        for _ in range(D[i]):
            J.append(random.randrange(A[i], A[i+1]))
    return(J)


def bonus_data(n) :
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["bonus"])
    bonus=data_df['bonus']
    bonus=bonus.values.tolist()
    m=(max(bonus)-min(bonus))/20
    l=[int(min(bonus)+((m*n)/19)) for n in range(19)]
    l.append(int(max(bonus)+1))
    B=[0 for i in range(20)]
    for elem in bonus:
        
        for i in range(20) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break
    
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def deferred_income_data(n) :
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["deferred_income"])
    deferred_income=data_df['deferred_income']
    deferred_income=deferred_income.values.tolist()
    a=max(deferred_income)
    b=min(deferred_income)
    m=(a-b)/10
    
    l=[int(b+(m*n)) for n in range(10)]
    l.append(int(a+1))
    a=l[len(l)-2]
    b=l[len(l)-1]
    for i in range(10) :
        l.pop()
        l.append(int(a+(i*(b-a)/10)))
    l.append(b)
    B=[0 for i in range(20)]
    for elem in deferred_income:   
        for i in range(20) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break
        
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def expenses_data(n) :  
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["expenses"])
    expenses=data_df['expenses']
    expenses=expenses.values.tolist()
    m=(max(expenses)-min(expenses))/20
    l=[int(min(expenses)+((m*n)/20)) for n in range(20)]
    l.append(int(max(expenses)+1))
    B=[0 for i in range(20)]
    for elem in expenses:
            
        for i in range(20) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break
        
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def total_payments_data(n) :  
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["total_payments"])
    total_payments=data_df['total_payments']
    total_payments=total_payments.values.tolist()
    m=(max(total_payments)-min(total_payments))/20
    l=[int(min(total_payments)+(m*n)/20) for n in range(20)]
    B=[0 for i in range(20)]
    l.append(int(max(total_payments)+1))
    for elem in total_payments:
        for i in range(20) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def deferral_payments_data(n) :         
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["deferral_payments"])
    deferral_payments=data_df['total_payments']
    deferral_payments=deferral_payments.values.tolist()
    m=(max(deferral_payments)-min(deferral_payments))/20
    l=[int(min(deferral_payments)+(m*n)/20) for n in range(20)]
    B=[0 for i in range(20)]
    l.append(int(max(deferral_payments)+1))
    for elem in deferral_payments:
        for i in range(20) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def total_stock_value_data(n) :
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["total_stock_value"])
    total_stock_value=data_df['total_stock_value']
    total_stock_value=total_stock_value.values.tolist()
    m=(max(total_stock_value)-min(total_stock_value))/30
    l=[int(min(total_stock_value)+(m*n)/30) for n in range(30)]
    B=[0 for i in range(30)]
    l.append(int(max(total_stock_value)+1))
    for elem in total_stock_value:
        for i in range(30) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def restricted_stock_data(n) :    
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["restricted_stock"])
    restricted_stock=data_df['restricted_stock']
    restricted_stock=restricted_stock.values.tolist()
    m=(max(restricted_stock)-min(restricted_stock))/30
    l=[int(min(restricted_stock)+(m*n)/30) for n in range(30)]
    B=[0 for i in range(30)]
    l.append(int(max(restricted_stock)+1))
    for elem in restricted_stock:
        for i in range(30) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def exercised_stock_options_data(n) : 
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["exercised_stock_options"])
    exercised_stock_options=data_df['exercised_stock_options']
    exercised_stock_options=exercised_stock_options.values.tolist()
    m=(max(exercised_stock_options)-min(exercised_stock_options))/30
    l=[int(min(exercised_stock_options)+(m*n)/30) for n in range(30)]
    B=[0 for i in range(30)]
    l.append(int(max(exercised_stock_options)+1))
    for elem in exercised_stock_options:
        for i in range(30) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def other_data(n) :    
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["other"])
    other=data_df['other']
    other=other.values.tolist()
    m=(max(other)-min(other))/30
    l=[int(min(other)+(m*n)/30) for n in range(30)]
    B=[0 for i in range(30)]
    l.append(int(max(other)+1))
    for elem in other:
        for i in range(30) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def long_term_incentive_data(n) :   
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["long_term_incentive"])
    long_term_incentive=data_df['long_term_incentive']
    long_term_incentive=long_term_incentive.values.tolist()
    m=(max(long_term_incentive)-min(long_term_incentive))/30
    l=[int(min(long_term_incentive)+(m*n)/30) for n in range(30)]
    B=[0 for i in range(30)]
    l.append(int(max(long_term_incentive)+1))
    for elem in long_term_incentive:
        for i in range(30) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)

def director_fees_data(n) :    
    data_df = pd.DataFrame.from_records(data).T
    data_df = data_df.apply (pd.to_numeric, errors='coerce')
    data_df=data_df.dropna(subset=["director_fees"])
    director_fees=data_df['director_fees']
    director_fees=director_fees.values.tolist()
    m=(max(director_fees)-min(director_fees))/5
    l=[int(min(director_fees)+(m*n)/5) for n in range(5)]
    B=[0 for i in range(5)]
    l.append(int(max(director_fees)+1))
    for elem in director_fees:
        for i in range(5) :
            if (elem<l[i+1]) and (elem>=l[i]) :
                B[i]+=1
                break 
    C = [round(n*(elem/sum(B))) for elem in B]
    J = []
    for i in range(len(C)):
        for _ in range(C[i]):
            J.append(random.randrange(l[i], l[i+1]))
    return(J)


def people_data(n) :
    people=pd.read_csv('People.csv',nrows=n)
    birthday=people['Birthday']
    birthday=birthday.values.tolist()
    occupation=people['Occupation']
    occupation=occupation.values.tolist()
    company=people['Company']
    company=company.values.tolist()
    vehicle=people['Vehicle']
    vehicle=vehicle.values.tolist()
    return birthday, occupation, company, vehicle
