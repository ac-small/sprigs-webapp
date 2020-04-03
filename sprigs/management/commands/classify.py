import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import seaborn as sns
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from sprigs.models import Product
from sprigs.models import Category
from sprigs.models import Product_Classification

# initialize prediction list
classified_datalist = []

def get_dataframe():
    """
    Read training dataset and save contents into a dataframe
    """
    df = pd.read_csv("./sprigs/management/commands/training_dataset.csv", encoding = "ISO-8859-1")
    df.head()
    return df

def retrieve_categories():
    """
    Query category table in database
    Return a list of all categories
    """
    categories = list(Category.objects.values_list('category', flat=True))
    return categories

def train_and_classify(df, categories, poultry_dataframe):
    train, test = train_test_split(df, random_state=42, test_size=0.33, shuffle=True)
    X_train = train.TEXT
    X_test = test.TEXT

    SVC_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(stop_words=stop_words)),
                    ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
                ])

    for category in categories:
        # train the model using X_train & categories
        training_model = SVC_pipeline.fit(X_train, train[category])
        # compute the testing accuracy
        prediction = training_model.predict(X_test)
        print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
        # run product data against trained model
        classified_datalist.append(predict_data(training_model, category, poultry_dataframe))

def predict_data(model, cat, poultry_dataframe):
    data_predictions = model.predict(poultry_dataframe.iloc[ : , 1 ])
    predictions = []
    for idx, val in enumerate(data_predictions):
        if str(val) == "1":
            predictions.append((poultry_dataframe.iloc[ idx , 0 ], cat))
    return predictions

def save_results_to_db(data):
    # Iterate over the array of tuples, create
    # classification objects, and persist to database
    for i in data:
        for record in i:
            print (record)
            Product_Classification.objects.bulk_create([
            Product_Classification(
            product_id = record[0],
            classification = record[1],
        )])


class Command(BaseCommand):
    help = 'Trains machine learning model, and predicts product classifications'

    def handle(self, *args, **options):
        """
        Retrieve category and product values from database
        Filter products by those containing price units (lbs/kg), and contains keywords chicken, turkey, or duck
        """
        categories = retrieve_categories()
        poultry_list = list(Product.objects.filter(price_units__isnull=False).filter(Q(product_name__icontains='CHICKEN')
            | Q(product_name__icontains='TURKEY')
            | Q(product_name__icontains='DUCK'))
            .values_list('flyer_id','product_name'))

        poultry_dataframe = pd.DataFrame(poultry_list)
        """
        Train model, classify results and save corresponding product classifications to database
        """
        training_dataframe = get_dataframe()
        train_and_classify(training_dataframe, categories, poultry_dataframe)
        save_results_to_db(classified_datalist)