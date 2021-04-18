#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import numpy as np
from sqlalchemy import create_engine
import pandas as pd


categories_filepath = 'disaster_categories.csv'
messages_filepath = 'disaster_messages.csv'
database_filename = '../db.sqlite3'
table_name ='disaster_message'

def load_data(messages_filepath, categories_filepath):
    """ Load & Merge messages & categories datasets
    inputs:
    messages_filepath: string. Filepath for csv file containing messages dataset.
    categories_filepath: string. Filepath for csv file containing categories dataset.
       
    outputs:
    df: dataframe. merge messages_filepath and categories_filepath
    
    """
    
    #Loaf Messages Dataset
    messages = pd.read_csv(messages_filepath)
    
    #Load Categories Dataset
    categories = pd.read_csv(categories_filepath)
    
    #Merge DataSets
    df = pd.merge(messages, categories, on = 'id')
    
    return df



def clean_data(df):
    ''' clean the data
    inputs:
        df (pandas.Dataframe): uncleaned data
    outputs:
        df(pandas.DataFrame): cleaned data
    '''
    categories = df.categories.str.split( ';',expand = True)
    row = categories.loc[0]
    category_colnames = [i[:-2] for i in row]
    categories.columns = category_colnames
    
    for column in categories:
        #set each value to be the last character of the string
        categories[column] = categories[column].str.split('-').str.get(1)
        #convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
    
    df.drop('categories',axis = 1,inplace = True)
    df = pd.concat([df, categories], axis=1)
    df = df.drop_duplicates()
    return df
        

def save_data(df, database_filename):
    '''Save the database. The table name is TABLE_NAME
    
    Inputs:
        df(pandas.dataframe): dataset
        database_filename : string database filename
    '''
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql(table_name,engine,index=False,if_exists = 'replace')

    
    


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '              'datasets as the first and second argument respectively, as '              'well as the filepath of the database to save the cleaned data '              'to as the third argument. \n\nExample: python process_data.py '              'disaster_messages.csv disaster_categories.csv '              'DisasterResponse.db')


if __name__ == '__main__':
    main()

