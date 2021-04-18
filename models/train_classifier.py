import nltk
nltk.download(['punkt', 'wordnet'])

# import libraries

import sys
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as db
import os
import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import classification_report,accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import confusion_matrix
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
import pickle


database_filepath = '../db.sqlite3'
table_name  = 'disaster_message'


def load_data(database_filepath,table_name):
    
    '''
    Inputs:
        database_filepath(str) : DisasterResponse.db
        table_name : disaster_message
    Outputs:
        X : messages
        y : categories
    '''
    engine = create_engine('sqlite:///' + database_filepath)
    df=pd.read_sql_table(table_name, engine)
    X = df['message']
    y = df.iloc[:,4:]
    category_names = list(df.columns[4:])
    return X,y, category_names
    
    
#X,y,category_names = load_data(database_filepath,table_name)                        



def tokenize(text):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model(grid_search_cv = False):
    '''
    Build the model
    Args:
        grid_search_cv (bool): if it is True then will be run. Grid Search run takes time so this method is added
    Returns:
        pipeline (pipeline.Pipeline): model
    '''
    pipeline = Pipeline([('vect', CountVectorizer(tokenizer = tokenize)), 
                     ('tfidf', TfidfTransformer()), 
                     ('clf', MultiOutputClassifier(RandomForestClassifier()))
                    ])

    #pipeline.get_params()

    if grid_search_cv == True:
        print('Searching for best parameters...')
        parameters = {'vect__ngram_range': ((1, 1), (1, 2))
            , 'vect__max_df': (0.5,  1.0)
            , 'tfidf__use_idf': (True, False)
            , 'clf__estimator__n_estimators': [50, 200]
            , 'clf__estimator__min_samples_split': [2, 4]
        }

        pipeline = GridSearchCV(pipeline, param_grid = parameters)

    return pipeline




def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Evaluate the model 
    Args:
        model (pipeline.Pipeline): model to evaluate
        X_test (pandas.Series): dataset
        Y_test (pandas.DataFrame): dataframe containing the categories
        category_names (str): categories name
    '''
    Y_pred = model.predict(X_test)
    # Calculate the accuracy for each of them.
    for i in range(len(category_names)):
       print('Category: {} '.format(category_names[i]))
       print(classification_report(Y_test.iloc[:, i].values, Y_pred[:, i]))
       print('Accuracy {}\n\n'.format(accuracy_score(Y_test.iloc[:, i].values, Y_pred[:, i])))
    


def save_model(model, model_filepath):
    '''
    Save in a pickle file the model
    Args:
        model: model to be saved
        model_pickle: pickle filename
    '''
    pickle.dump(model, open(model_filepath, 'wb'))





    
def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath,table_name)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model(grid_search_cv = False)
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
