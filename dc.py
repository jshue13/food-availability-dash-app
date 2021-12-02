### This file includes code for cleaning and preparing the data for Dash application ###
import pandas as pd
import numpy as np

# Function to remove the Notes column, set the correct data types, and remove rows with NaN or special characters
def format_data(data_filename):
    data = pd.read_csv(data_filename) # takes in a CSV file
    data.drop('Notes', axis=1, inplace=True)
    data['Commodity'] = data['Commodity'].str.lower()
    data['Attribute'] = data['Attribute'].str.lower().str.strip()
    data.dropna(axis=0, inplace=True) # drop rows with NaN
    data = data.loc[data['Value'] != '*'] # remove rows with '*'
    data = data.loc[data['Value'] != '-'] # remove rows with '-'
    data = data.loc[data['Value'] != '--'] # remove rows with '--'
    data = data.loc[data['Value'] != '--  '] # remove rows with '--  '
    data["Value"] = data['Value'].astype('float') # cast Value column as float
    return data

### Data Preparation for the Dairy Products Dataset ###
dairy_prod_temp = format_data('data/dymfg.csv')

# Only get rows that have 'per capita availability' in the Commodity column. Exclude rows that have 'butterfat' in the commodity name.
dairy_prod_temp = dairy_prod_temp.loc[dairy_prod_temp['Commodity'].str.contains('per capita availability')&~dairy_prod_temp['Commodity'].str.contains('butterfat')]

# Only get rows that the following keywords in the Attribute column and does not include the term 'sales'.
keywords = ['butter-pounds', 'fluid milk-pounds', 'per capita-pounds', 'all dairy products, milk-fat milk-equivalent basis-pounds']
dairy_prod_temp = dairy_prod_temp.loc[dairy_prod_temp['Attribute'].str.contains('|'.join(keywords))&~dairy_prod_temp['Attribute'].str.contains('sales')]

# Further filter the rows with the following keywords and excluding other terms.
keywords = ['fluid milk', 'all', 'butter', 'yogurt', 'sour cream', 'total', 'dried whey']
excludes = ['whole', 'buttermilk', 'frozen yogurt']
dairy_prod_temp = dairy_prod_temp.loc[dairy_prod_temp['Attribute'].str.contains('|'.join(keywords))&~dairy_prod_temp['Attribute'].str.contains('|'.join(excludes))]

# Rename the Attribute categories by removing unnecessary characters and transforming into Title case
dairy_prod_temp['Attribute'] = dairy_prod_temp['Attribute'].str.replace(r"\-.+","",regex=True)
dairy_prod_temp['Attribute'] = dairy_prod_temp['Attribute'].str.replace('|'.join(['total',', milk']),"",regex=False)
dairy_prod_temp['Attribute'] = dairy_prod_temp['Attribute'].str.title().str.strip()

# Note that this data set needs to be updated to include Cheese PCC; this will require manual calculations from the raw data

dairy_prod_pcc = dairy_prod_temp
dairy_prod = dairy_prod_pcc['Attribute'].unique()
years = dairy_prod_pcc.Year.unique()


### Data Preparation for the Eggs Dataset ###
eggs_temp = format_data('data/eggs.csv')

eggs_temp = eggs_temp.loc[eggs_temp['Commodity'].str.contains('per capita availability')]
eggs_temp = eggs_temp.loc[eggs_temp['Attribute'].str.contains('per capita-number')]
eggs_temp['Attribute'].replace(['shell-per capita-number','total-retail weight-number-per capita-number',
                                'processed-per capita-number', 'total-farm weight-number-per capita-number'],
                                ['Shell', 'Total (Retail)', 'Processed', 'Total (Farm)'], inplace=True)
eggs_pcc = eggs_temp
egg_prod = eggs_pcc.Attribute.unique()


### Data Preparation for the Produce Dataset ###
produce_temp = format_data('data/fruitveg.csv')

def prod_agg(x):
    if 'vegetables-fresh-pounds' in x:
        return 'Total'
    elif 'fruit-fresh-pounds' in x:
        return 'Total'
    elif 'total' in x:
        return 'Total'

def prod_cat(x):
    if 'total fruit and vegetables-pounds' in x:
        return 'Total'
    elif 'fruit' in x:
        return 'Fruit'
    elif 'vegetable' in x:
        return 'Vegetable'

def prod_type(x):
    if 'fresh' in x:
        return 'Fresh'
    elif 'process' in x:
        return 'Processed'

produce_temp['Aggregation'] = produce_temp['Attribute'].apply(prod_agg)
produce_temp['Category'] = produce_temp['Attribute'].apply(prod_cat)
produce_temp['Type'] = produce_temp['Attribute'].apply(prod_type)

produce_attr = produce_temp.Attribute.unique().tolist()
# print(type(prod_attr))
produce_attr_new = ['Fresh Fruit', 'Canned Fruit', 'Frozen Fruit', 'Dried Fruit', 'Juice', 'Other Processed Fruit', 'Total Processed Fruit', 'Total Fruit',
                    'Fresh Vegetables', 'Canned Vegetables', 'Frozen Vegetables', 'Dried Vegetables', 'Potatoes for Chips', 'Legumes', 'Total Processed Vegetables',
                    'Total Vegetables', 'Total Fruit and Vegetables']
produce_temp['Product'] = produce_temp['Attribute'].replace(produce_attr, produce_attr_new)
# print(produce_temp.iloc[:,1:].tail(20))
produce_pcc = produce_temp


### Data Preparation for the Grain Dataset ###
grains_temp = format_data('data/grains.csv') # initial data formatting

# only get rows that have 'per capita availability' in the Commodity column
grains_temp = grains_temp.loc[grains_temp['Commodity'].str.contains('per capita availability')]

# rename so that historical data is included correctly
grains_temp['Attribute'].replace(['pounds'],['total flour and cereal products-pounds'], inplace=True) 

# addtional formatting
grains_temp['Attribute'] = grains_temp['Attribute'].str.replace('-pounds',"",regex=False)
grains_temp['Attribute'] = grains_temp['Attribute'].str.title().str.strip()
grains_temp.sort_values("Year", inplace=True) # sort by years so that the historical data is aligned

# set data to be used in components and callbacks
grains_pcc = grains_temp
grains_prod = grains_pcc.Attribute.unique()

