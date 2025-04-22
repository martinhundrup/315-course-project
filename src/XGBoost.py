from xgboost import XGBClassifier
from xgboost import XGBRegressor
# read data
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,mean_squared_error,r2_score
from category_encoders.target_encoder import TargetEncoder
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
import pandas as pd
import numpy as np
import time as t
import os




class XGBoostModel:
    def __init__(self):
        self.pipeline = None
        self.search_space = None
        self.opt = None
        self.X = None
        self.Y = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.dataframe = None
        self.original_df = None # after the nan values have been dropped
        self.dataframe = pd.read_csv("./src/ppdata.csv")

    """Just our base test for XG Boost given within the documentation"""
    def test_xg_boost(self):
        data = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=.2)
        # create model instance
        bst = XGBClassifier(n_estimators=2, max_depth=2, learning_rate=1, objective='binary:logistic')
        # fit model
        bst.fit(X_train, y_train)
        # make predictions
        preds = bst.predict(X_test)

        print(data['data'])
        print(preds)

    """Cleans the data based on the data frame, they should all look similar
       Drop any columns you want before """
    def data_cleaner(self, dataframe, columns_to_drop):
        dataframe = dataframe.dropna()
        dataframe = dataframe.reset_index(drop=True)
        self.original_df = dataframe
        #self.dataframe = self.dataframe.fillna(0) # <- this is bad, want to find a better way to do this
        #print(dataframe.columns)
        dataframe = dataframe.drop(columns=columns_to_drop)
        return dataframe
        print(len(dataframe))

    """ Reads our data 
        Model is trained using X to Predict Y 
        X is all current Data"""
    def train_covid_deaths(self, dataframe, prediction_data, columns_to_drop):
        #self.dataframe = pd.read_csv("./src/ppdata.csv")
       
        dataframe = self.data_cleaner(dataframe, columns_to_drop)

        # Our Featues, Currently Just COVID Deaths
        self.X = dataframe.drop(columns=[prediction_data])

        self.Y = dataframe[prediction_data]
        
        # Our training and testing set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=8)

    """Standard Preprocessing feature for ML"""
    def training_pipeline(self):
        estimators = [
            ('encoder', TargetEncoder()),
            ('clf', XGBRegressor(random_state=8)) # for resuable data points
        ]
        self.pipe = Pipeline(steps=estimators)

    """Tuning for the model"""
    def hyperparameter_tuning(self):
        search_space = {
            'clf__max_depth': Integer(2,10),
            'clf__learning_rate': Real(0.001, 0.2, prior='log-uniform'),
            'clf__subsample': Real(0.5, 1.0),
            'clf__colsample_bytree': Real(0.5, 1.0),
            'clf__colsample_bylevel': Real(0.5, 1.0),
            'clf__colsample_bynode': Real(0.5, 1.0),
            'clf__reg_alpha': Real(0.0, 10),
            'clf__reg_lambda': Real(0.0, 10),
            'clf__gamma': Real(0.0, 10),
        }

        self.search_space = search_space
        opt = BayesSearchCV(self.pipe, self.search_space, cv=5, n_iter=75, scoring='neg_mean_squared_error', random_state=8)
        self.opt = opt

    """Fits the model"""
    def train_xgboost_model(self):
        self.opt.fit(self.X_train, self.y_train)
    
    """This function just prints out all of our prediction scores for us to see"""
    def evaluate_make_predictions(self):
        print(self.opt.score(self.X_test, self.y_test))
        county_deaths = self.opt.predict(self.X_test)
        # for i in range(len(county_deaths)):
        #     print(f"Predicted Death Total for {self.dataframe['County'][i]}: {county_deaths[i]:.2f}, Actual Death Total: {self.dataframe['COVID Deaths'][i]}")
        #     #print(f"Actual Death Total for {self.dataframe['County'][i]}: {self.dataframe['COVID Deaths'][i]}")
        #     print("="*50)

        #print(len(self.X_train))
        #print(len(county_deaths))

        print(f"Negative Mean Squared Error: {self.opt.score(self.X_test, self.y_test)}")
        #print(f"Accuracy: {accuracy_score(self.y_test, county_deaths)}")
        print(f"R^2 Score: {r2_score(self.y_test, county_deaths)}")
        print(f"Mean Squared: {mean_squared_error(self.y_test, county_deaths)}")

    def print_out_predictions(self):
        all_county_predictions = self.opt.predict(self.X)
        all_county_predictions = np.round(all_county_predictions)
        # for i in range(len(all_county_predictions)):
        #     print(f"Predicted Death Total for {self.dataframe['County'][i]}: {all_county_predictions[i]:.1f}, Actual Death Total: {self.dataframe['COVID Deaths'][i]}")
        #     print(f"Actual Death Total for {self.dataframe['County'][i]}: {self.dataframe['COVID Deaths'][i]}")
        #     print("="*50)

        # print(len(all_county_predictions))

    """Going to want CSV to display 
       Predicted Deaths, 
       Actual Deaths,
       Percent In Change between Predicted / Actual -val if below +val if above
       Going to Create two CSV's, one with the full data set
       The other with just predicted outcomes for each county.
       """
    def write_to_csv(self, operation):

        all_county_predictions = self.opt.predict(self.X)
        all_county_predictions = np.round(all_county_predictions)

        # Define the output directory
        output_dir = "Predicted Data"
        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        match operation:
            case "Only Deaths":

                # Construct full file paths
                full_data_path = os.path.join(output_dir, 'Deaths-All-Data-And-Predicted.csv')
                short_data_path = os.path.join(output_dir, 'Deaths-Shortened-Data.csv')

                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#
                self.original_df['Predicted COVID Deaths'] = all_county_predictions
                self.original_df['Amount Over / Under (Deaths)'] = all_county_predictions - self.original_df['COVID Deaths']
                self.original_df.to_csv(full_data_path, index=False)
                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#

                #============================ Shortened Data ============================#
                new_df = self.original_df[['FIPS', 'State', 'County', 'COVID Deaths', 'Predicted COVID Deaths', 'Amount Over / Under (Deaths)', 'Population']]
                new_df.to_csv(short_data_path, index=False)
                #============================ Shortened Data ============================#

            case "Only Cases":

                # Construct full file paths
                full_data_path = os.path.join(output_dir, 'Cases-All-Data-And-Predicted.csv')
                short_data_path = os.path.join(output_dir, 'Cases-Shortened-Data.csv')

                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#
                self.original_df['Predicted COVID Cases'] = all_county_predictions
                self.original_df['Amount Over / Under (Cases)'] = all_county_predictions - self.original_df['COVID Cases']
                self.original_df.to_csv(full_data_path, index=False)
                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#

                #============================ Shortened Data ============================#
                new_df = self.original_df[['FIPS', 'State', 'County', 'Predicted COVID Cases', 'Amount Over / Under (Cases)', 'Population']]
                new_df.to_csv(short_data_path, index=False)
                #============================ Shortened Data ============================#
            case "Predicted Deaths and Cases":

                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#
                self.original_df['Predicted COVID Deaths'] = all_county_predictions
                self.original_df['Amount Over / Under (Deaths)'] = all_county_predictions - self.original_df['COVID Deaths']
                self.original_df.to_csv('Deaths-All-Data-And-Predicted.csv', index=False)
                #============================ ALL DATA WITH AMOUNT OVER / UNDER ============================#

                #============================ Shortened Data ============================#
                new_df = self.original_df[['FIPS', 'State', 'County', 'COVID Deaths', 'Predicted COVID Deaths', 'Amount Over / Under (Deaths)', 'Population']]
                new_df.to_csv('Deaths-Shortened-Data.csv', index=False)
                #============================ Shortened Data ============================#



    # Pass in dataframe, then what we want to train, then file type

    """This is what will run the whole model for you based on some parameters you put in
        dataframe= your data
        train_data= pass in a literal string of a column to train on
        operation= what you want to write out to the csv
        columns_to_drop= what columns you want to be removed before training is started / 
                         noisy columns"""
    def run_all(self, dataframe, train_data, operation, columns_to_drop):
        start = t.time()
        self.train_covid_deaths(dataframe, train_data, columns_to_drop)
        self.training_pipeline()
        self.hyperparameter_tuning()
        self.train_xgboost_model()
        end = t.time()
        print(f"Total Model Time In Minuets: {((end - start) / 60):.2f}")
        self.evaluate_make_predictions()
        self.print_out_predictions()
        self.write_to_csv(operation)

x = XGBoostModel()

dataframe = pd.read_csv("./src/ppdata.csv")

x.run_all(dataframe, 'COVID Cases', 'Only Cases', ['FIPS', 'State'])