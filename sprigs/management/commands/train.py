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


def get_dataframe():
    df = pd.read_csv("./sprigs/management/commands/training_dataset.csv", encoding = "ISO-8859-1")
    df.head()
    return df

def train_and_classify(df, poultry_dataframe):
    categories = ['Chicken Breast Boneless Skinless','Chicken Whole Birds (Fresh)','Chicken Whole Birds (Frozen)','Chicken Drumsticks','Chicken Leg Quarters','Chicken Leg','Chicken Thigh Boneless Skinless','Chicken Wings','Chicken Breast Bone-In Skin-On','Chicken Thigh Bone-In Skin-On']
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
        # predict external data
        ext_preds = predict_data(training_model, category, poultry_dataframe)
        print (ext_preds)

def predict_data(model, cat, poultry_dataframe):
    data_predictions = model.predict(poultry_dataframe.iloc[ : , 1 ])
    predictions = []
    for idx, val in enumerate(data_predictions):
        if str(val) == "1":
            predictions.append((poultry_dataframe.iloc[ idx , 0 ], cat))
    return predictions

class Command(BaseCommand):
    help = 'Trains machine learning model, and predicts product classifications'

    def handle(self, *args, **options):
        """
        Filter products by those containing price units (lbs/kg), and contains keywords chicken, turkey, or duck
        Returns: List of product objects (flyer_id, and product_name)
        """
        poultry_list = list(Product.objects.filter(price_units__isnull=False).filter(Q(product_name__icontains='CHICKEN')
            | Q(product_name__icontains='TURKEY')
            | Q(product_name__icontains='DUCK'))
            .values_list('flyer_id','product_name'))

        poultry_dataframe = pd.DataFrame(poultry_list)

        training_dataframe = get_dataframe()
        train_and_classify(training_dataframe, poultry_dataframe)
