#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv(r'datasets/dataset-3.csv')


# In[3]:


df.head(5)


# ## Question 1: Distance Matrix Calculation
# 
# Create a function named `calculate_distance_matrix` that takes the `dataset-3.csv` as input and generates a DataFrame representing distances between IDs. 
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0.
# If distances between toll locations A to B and B to C are known, then the distance from A to C should be the 
# sum of these distances. 
# Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A). 
# 
# Sample result dataframe:\
#  ![Task 2 Question 1](readme_images/task2-q1.png)
# 
# 

# In[4]:


def calculate_distance_matrix (df):
    matrix=pd.pivot_table(df, values='distance', index=['id_start'],
                       columns=['id_end'], fill_value=0)
    return matrix
    

calculate_distance_matrix (df)  


# ## Question 2: Unroll Distance Matrix
# 
# Create a function `unroll_distance_matrix` that takes the DataFrame created in Question 1. 
# The resulting DataFrame should have three columns: columns `id_start`, `id_end`, and `distance`.
# 
# All the combinations except for same `id_start` to `id_end` must be present in the 
# rows with their distance values from the input DataFrame.
# 
# 

# In[5]:


def unroll_distance_matrix (df):
    matrix=pd.pivot_table(df, values='distance', index=['id_start'],
                       columns=['id_end'], fill_value=0)
    df2=pd.melt(matrix,ignore_index=False)
    df2.reset_index(level=0,inplace=True)
    df2=df2[df2['id_start']!=df2['id_end']]
    
    return df2

unroll_distance_matrix (df) 


# ## Question 3: Finding IDs within Percentage Threshold
# 
# Create a function `find_ids_within_ten_percentage_threshold` that takes the DataFrame created in Question 2 
# and a reference value from the `id_start` column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values 
# from `id_start` column which lie within 10% (including ceiling and floor) of the reference value's average.
# 
# 

# In[6]:


def find_ids_within_ten_percentage_threshold(df):
    matrix=pd.pivot_table(df, values='distance', index=['id_start'],
                       columns=['id_end'], fill_value=0)
    df2=pd.melt(matrix,ignore_index=False)
    df2.reset_index(level=0,inplace=True)
    df2=df2[df2['id_start']!=df2['id_end']]
    df3=df2.groupby('id_start')['value'].mean()
    sorted_list=[]
    for x in df3.values:
         if x <= df3.values.mean()*0.10:
                sorted_list.append(x)
    return sorted_list
        
   

    
find_ids_within_ten_percentage_threshold(df)


# ## Question 4: Calculate Toll Rate
# 
# Create a function `calculate_toll_rate` that takes the DataFrame created in Question 2 as input and 
# calculates toll rates based on vehicle types. 
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: `moto`, `car`, `rv`, `bus`, and `truck`
#     with their respective rate coefficients. The toll rates should be calculated by multiplying the distance 
#     with the given rate coefficients for each vehicle type: 
# - 0.8 for `moto`
# - 1.2 for `car`
# - 1.5 for `rv`
# - 2.2 for `bus`
# - 3.6 for `truck`
# 
# Sample result dataframe:\
#  ![Task 2 Question 4](readme_images/task2-q4.png)
# 
# 

# In[7]:


def calculate_toll_rate(df):
    df['moto']=df['distance']*0.8
    df['car']=df['distance']*1.2
    df['rv']=df['distance']*1.5
    df['bus']=df['distance']*2.2
    df['truck']=df['distance']*3.6
    df1=df[['id_start','id_end','moto','car','rv','bus','truck']]
    return df1
calculate_toll_rate(df)


# ## Question 5: Calculate Time-Based Toll Rates
# 
# Create a function named `calculate_time_based_toll_rates` that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day. 
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# - `start_day`, `end_day` must be strings with day values (from Monday to Sunday in proper case)
# - `start_time` and `end_time` must be of type datetime.time() with the values from time range given below.
# 
# Modify the values of vehicle columns according to the following time ranges:
# 
# **Weekdays (Monday - Friday):**
# - From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# - From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# - From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# 
# **Weekends (Saturday and Sunday):**
# - Apply a constant discount factor of 0.7 for all times.
# 
# For each unique (`id_start`, `id_end`) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Sample result dataframe:\
#  ![Task 2 Question 5](readme_images/task2-q5.png)

# In[8]:


matrix=pd.pivot_table(df, values='distance', index=['id_start'],
                       columns=['id_end'], fill_value=0)
df2=pd.melt(matrix,ignore_index=False)
df2.reset_index(level=0)

df2.groupby(['id_start','id_end']).sum().head(50)

