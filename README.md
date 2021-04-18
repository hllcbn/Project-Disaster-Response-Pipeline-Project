# Project:  Disaster Response Pipeline Project

### Table of Contents
•	[Motivation](#Motivation)

•	[Descriptions](#Description)

•	[Instruction](#Instruction)

•	[Installation](#Installation)

•	[Data](#Data)

•	[Result](#Result)

•	[Licensing, Authors, and Acknowledgements](#Licensing)

## Motivation <a name="Motivation"></a>

This Project is part of Udacity Data Science Nanodegree Program . The dataset contains messages from disaster. The goal of the project is to build a Natural Language Processing tool and classify the disaster messages into categories. The web app also displays visualizations of the data

## Descriptions <a name="Descriptions"></a>
The Project is divided in the following Sections:

1.	**ETL Pipeline:**  Data Processing, ETL Pipeline to extract , clean  and save data  in a proper database structure.

2.	**ML Pipeline:**  Machine Learning Pipeline to train a model able to classify text message in categories.

3.	**Flask Web App:**  Web App to show model results in real time.

## Instruction <a name="Instruction"></a>

To execute the app follow the instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/



## Installation <a name="Installation"></a>

This project requires Python 3.x and the following Python libraries installed:

•	pandas

•	re

•	sys

•	json

•	html

•	sklearn

•	nltk

•	sqlalchemy

•	pickle

•	Flask

•	plotly

•	sqlite3


## Data <a name="Data"></a>

The dataset is provided by Figure Eight is basically composed by:

•	disaster_categories.csv: Categories of the messages

•	disaster_messages.csv: Multilingual disaster response messages


## Result: Screenshots <a name="Result: Screenshots"></a>

1.The content of the Web app shows disaster messages.

![image](https://user-images.githubusercontent.com/59744578/115153223-6fd96e80-a03a-11eb-8be4-a189cbc13042.png)

2.	You can see the categories that the messages belong to highlighted  in green after clicking classify message.

![image](https://user-images.githubusercontent.com/59744578/115153584-66510600-a03c-11eb-8b8e-a814d3a4c717.png)

3.	In the first page, you can see three different graphs giving information about messages categories

![image](https://user-images.githubusercontent.com/59744578/115153594-749f2200-a03c-11eb-9eec-dc601252261d.png)

## Licensing, Authors, and Acknowledgements
Credit to Figure Eight for the datasets and more information about licensing of the data can be find [here.](https://appen.com/open-source-datasets/)


