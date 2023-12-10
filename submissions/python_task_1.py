#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv(r'datasets/dataset-1.csv')


# In[3]:


df.head(5)


# ## Question 1: Car Matrix Generation
# Under the function named `generate_car_matrix` write a logic that takes the `dataset-1.csv` as a DataFrame. Return a new DataFrame that follows the following rules:
# - values from `id_2` as columns
# - values from `id_1` as index
# - dataframe should have values from `car` column
# - diagonal values should be 0.

# In[4]:


def generate_car_matrix (df):
    matrix=pd.pivot_table(df, values='car', index=['id_1'],
                       columns=['id_2'], fill_value=0)
    return matrix
    

generate_car_matrix (df)    
    
    


# ## Question 2: Car Type Count Calculation
# Create a Python function named `get_type_count` that takes the `dataset-1.csv` as a DataFrame. Add a new categorical column `car_type` based on values of the column `car`:
# - `low` for values less than or equal to 15,
# - `medium` for values greater than 15 and less than or equal to 25,
# - `high` for values greater than 25.
# 
# Calculate the count of occurrences for each `car_type` category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.
# 

# In[5]:


def get_type_count(df):
    df['car_type'] = ['low' if x <= 15 else 'medium' if x > 15 and x<=25  else 'high' for x in df['car']]
    count_dict=df['car_type'].value_counts().to_dict()
    Keys = list(count_dict.keys())
    Keys.sort()
    sorted_dict = {i: count_dict[i] for i in Keys}
    
    return sorted_dict


get_type_count(df)

    


# ## Question 3: Bus Count Index Retrieval
# 
# Create a Python function named `get_bus_indexes` that takes the `dataset-1.csv` as a DataFrame. The function should identify
# and return the indices as a list (sorted in ascending order)
# where the `bus` values are greater than twice the mean value of the `bus` column in the DataFrame.
# 
# 

# In[6]:


def get_bus_indexes(df):
    twice_of_mean=df['bus'].mean()*2
    list1=df[df['bus'] > twice_of_mean].index.to_list()
    
    return list1

get_bus_indexes(df)
    
    


# ## Question 4: Route Filtering
# Create a python function `filter_routes` that takes the `dataset-1.csv` as a DataFrame. 
# The function should return the sorted list of values of column `route` for which the average of values of `truck` column 
# is greater than 7.
# 
# 

# In[7]:


def filter_routes (df):
    filtered_routes=list((df.groupby('route')['truck'].mean()>7).index)
    return filtered_routes

filter_routes (df)


# ## Question 5: Matrix Value Modification
# 
# Create a Python function named `multiply_matrix` that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# - If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# - If a value is 20 or less, multiply those values by 1.25.
# 
# The function should return the modified DataFrame which has values rounded to 1 decimal place.
# 
# Sample result dataframe:\
#  ![Task 1 Question 5](readme_images/task1-q5.png)
# 
# 

# In[8]:


def multiply_matrix (df):
    matrix=pd.pivot_table(df, values='car', index=['id_1'],columns=['id_2'], fill_value=0)
    df_1=pd.melt(matrix,ignore_index=False)
    df_1.reset_index(level=0,inplace=True)
    f=(lambda x: x*0.57 if x>20 else x*1.25)
    df_1['multiply']=df_1['value'].apply(f)
    multiplied_matrix= pd.pivot_table(df_1, values='multiply', index=['id_1'],columns=['id_2'], fill_value=0)
    
    return multiplied_matrix



    
multiply_matrix (df)
    


# ## Question 6: Time Check
# 
# You are given a dataset, `dataset-2.csv`, containing columns `id`, `id_2`, 
# and timestamp (`startDay`, `startTime`, `endDay`, `endTime`). 
# The goal is to verify the completeness of the time data by checking whether the timestamps for
# each unique (`id`, `id_2`) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) 
# and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts `dataset-2.csv` as a DataFrame and 
# returns a boolean series that indicates if each (`id`, `id_2`) pair has incorrect timestamps. 
# The boolean series must have multi-index (`id`, `id_2`).
# 

# In[9]:


df2=pd.read_csv(r'datasets/dataset-2.csv')


# In[10]:


df2


# In[11]:


df3=df2[['id','id_2','startDay','startTime','endDay','endTime']]


# In[12]:


df3['pair'] = df3[['id', 'id_2']].apply(tuple, axis=1)


# In[13]:


df3.sort_values(by='pair')


# In[14]:


df3[df3['pair']==(1069022, -1)].head(50)


# In[15]:


type(df3.pair.value_counts())


# In[16]:


x=pd.DataFrame({'pair':df3.pair.value_counts().index,'count':df3.pair.value_counts().values})


# In[17]:


x[x['count']==3]

