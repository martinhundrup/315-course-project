from xgboost import XGBClassifier
from xgboost import XGBRegressor
# read data
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from category_encoders.target_encoder import TargetEncoder
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
import pandas as pd


class XGBoostModel:
    def __init__(self):
        self.pipeline = None
        self.search_space = None
        self.opt = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.dataframe = None

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

    """ Reads our data """
    def train_covid_deaths(self):
        self.dataframe = pd.read_csv("./src/ppdata.csv")
        self.dataframe = self.dataframe.fillna(0)
        #print(dataframe.columns)
        X = self.dataframe.drop(columns="COVID Deaths")
        #print(X.columns)
        Y = self.dataframe['COVID Deaths']

        # Our training and testing set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, Y, test_size=0.2, random_state=8)

    """Standard Preprocessing feature for ML"""
    def training_pipeline(self):
        estimators = [
            ('encoder', TargetEncoder()),
            ('clf', XGBRegressor(random_state=8)) # for resuable data points
        ]
        self.pipe = Pipeline(steps=estimators)

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

    def train_xgboost_model(self):
        self.opt.fit(self.X_train, self.y_train)
    
    def evaluate_make_predictions(self):
        print(self.opt.score(self.X_test, self.y_test))
        county_deaths = self.opt.predict(self.X_test)
        for i in range(len(county_deaths)):
            print(f"Predicted Death Total for {self.dataframe['County'][i]}: {county_deaths[i]:.2f}")
            print(f"Actual Death Total for {self.dataframe['County'][i]}: {self.dataframe['COVID Deaths'][i]}")
            print("="*50)

    def run_all(self):
        self.train_covid_deaths()
        self.training_pipeline()
        self.hyperparameter_tuning()
        self.train_xgboost_model()
        self.evaluate_make_predictions()

x = XGBoostModel()

x.run_all()