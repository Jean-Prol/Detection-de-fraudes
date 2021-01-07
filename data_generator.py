from data_utils import *
import numpy as np

def generate_dataframe(n): 
    property=property_data(n)
    
    income=income_data(n)
    if len(income)<n :
        income+=[np.nan for i in range(n-len(income))]
    if len(income)>n :
        income=income[:n]
    property['income']=income
        
    deferred_income=deferred_income_data(n) 
    if len(deferred_income)<n :
        deferred_income+=[np.nan for i in range(n-len(deferred_income))]
    if len(deferred_income)>n :
        deferred_income=deferred_income[:n]
    property['deferred_income']=deferred_income
    
    bonus=bonus_data(n)
    if len(bonus)<n :
        bonus+=[np.nan for i in range(n-len(bonus))]
    if len(bonus)>n :
        bonus=bonus[:n]
    property['bonus']=bonus
    
    total_payments=total_payments_data(n)
    if len(total_payments)<n :
        total_payments+=[np.nan for i in range(n-len(total_payments))]
    if len(total_payments)>n :
        total_payments=total_payments[:n]
    property['total_payments']=total_payments
    
    deferral_payments=deferral_payments_data(n) 
    if len(deferral_payments)<n :
        deferral_payments+=[np.nan for i in range(n-len(deferral_payments))]
    if len(deferral_payments)>n :
        deferral_payments=deferral_payments[:n]
    property['deferral_payments']=deferral_payments
    
    total_stock_value=total_stock_value_data(n)
    if len(total_stock_value)<n :
        total_stock_value+=[np.nan for i in range(n-len(total_stock_value))]
    if len(total_stock_value)>n :
        total_stock_value=total_stock_value[:n]
    property['total_stock_value']=total_stock_value
        
    restricted_stock=restricted_stock_data(n) 
    if len(restricted_stock)<n :
        restricted_stock+=[np.nan for i in range(n-len(restricted_stock))]
    if len(restricted_stock)>n :
        restricted_stock=restricted_stock[:n]
    property['restricted_stock']=restricted_stock
        
    exercised_stock_options=exercised_stock_options_data(n)
    if len(exercised_stock_options)<n :
        exercised_stock_options+=[np.nan for i in range(n-len(exercised_stock_options))]
    if len(exercised_stock_options)>n :
        exercised_stock_value=exercised_stock_value[:n]
    property['exercised_stock_options']=exercised_stock_options
    
    other=other_data(n)
    if len(other)<n :
        other+=[np.nan for i in range(n-len(other))]
    if len(other)>n :
        other=other[:n]
    property['other']=other    
        
    long_term_incentive=long_term_incentive_data(n)
    if len(long_term_incentive)<n :
        long_term_incentive+=[np.nan for i in range(n-len(long_term_incentive))]
    if len(long_term_incentive)>n :
        long_term_incentive=long_term_incentive[:n]
    property['long_term_incentive']=long_term_incentive
        
    director_fees=director_fees_data(n)
    if len(director_fees)<n :
        director_fees+=[np.nan for i in range(n-len(director_fees))]
    if len(director_fees)>n :
        director_fees=director_fees[:n]
    property['director_fees']=director_fees
    
    expenses=expenses_data(n)
    if len(expenses)<n :
        expenses+=[np.nan for i in range(n-len(expenses))]
    if len(expenses)>n :
        expenses=expenses[:n]
    property['expenses']=expenses
    
    property=property.dropna(subset=['other','expenses','director_fees','long_term_incentive', 
                                     'exercised_stock_options','restricted_stock','total_stock_value', 
                                     'deferral_payments','total_payments','bonus','deferred_income','income'])
    a=len(property['expenses'])
    birthday, occupation, company, vehicle=people_data(a)
    property['birthday']=birthday
    property['occupation']=occupation
    property['company']=company
    property['vehicle']=vehicle
    return(property)

def label_data(data) :
    n=len(data['expenses'])
    l=np.random.randint(2, size=n)
    data['fraud']=l
    return(data)

def generate_database(n) :
    data=label_data(generate_dataframe(n))
    data.to_csv(r'labeled_database.tsv', sep='\t')
    
    
    