import pandas as pd

def order(frame,var):
    if type(var) is str:
        var = [var] #let the command take a string or list
    varlist =[w for w in frame.columns if w not in var]
    frame = frame[var+varlist]
    return frame 

df_cap = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure\cap.csv')
df_pop = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure\israel pop.csv')
df_budget = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure\budget.csv', index_col = 'Year')
df_hpi = pd.read_csv(r'C:\Users\User\Documents\Projects\Health Expenditure\hpi.csv', index_col = 'Year')

df_pop = df_pop.pivot(index = 'Year', columns = 'Age', values = 'Population')

df_pop = order(df_pop, '0_4')

df_new_pop = pd.DataFrame(columns = df_cap['Age'])

df_new_pop['0_4'] = df_pop['0_4']
df_new_pop['85_OVER'] = df_pop['85_OVER']

c = 1
for i in df_new_pop.columns[1:-1]:
    df_new_pop[i] = df_pop.iloc[:, c] + df_pop.iloc[:, c+1]
    c += 2

df_cap.set_index('Age', inplace = True)
for i in df_cap.index:
    df_new_pop[i] *= df_cap.loc[i, 'Cap']

df_new_pop['TOTAL'] = df_new_pop.sum(axis = 1)

df_budget['Per Capita'] = df_budget['Value']/df_pop['TOTAL']*1000000
df_budget['Per Capita Age Standardized'] = df_budget['Value']/df_new_pop['TOTAL']*1000000
df_budget['Per Capita Real Age Standardized'] = df_budget['Per Capita Standardized']/df_hpi['HPI']*100

df_budget.to_csv(r'C:\Users\User\Documents\Projects\Health Expenditure\results.csv')
