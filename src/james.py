import pandas as pd
import numpy as np



allData = pd.read_csv("./src/ppdata.csv")
allData = allData.drop(columns = ["State","County","FIPS"])

allData.corr().to_csv("Coorelation-Population.csv")


allData = allData.drop(columns = ["Poverty Raw","Unemployed",
                        "Less than high school graduate, 2019-23",
        "High school graduate (or equivalency), 2019-23",
        "Some college or associate degree, 2019-23",
        "Bachelor's degree or higher, 2019-23"
                        ])
allData = allData.dropna()
percentCasesDeaths = allData["COVID Deaths"].div(allData["COVID Cases"])#.rename("Percent Deaths of Cases"))
allData[[
    "COVID Cases","COVID Deaths","Labor Force","Employed",
         ]] = allData[[
    "COVID Cases","COVID Deaths","Labor Force","Employed",
         ]].div(allData["Population"], axis = 0)
allData = allData.drop(columns = ["Population"])
#print(allData.corr())
allData.insert(1, "Percent Deaths of Cases",percentCasesDeaths)
allData.corr().to_csv("Coorelation-Percent.csv")
#allData = allData.drop(columns = ["Poverty Raw","Labor Force","Less than high school graduate, 2019-23","High school graduate (or equivalency), 2019-23","Some college or associate degree, 2019-23","Bachelor's degree or higher, 2019-23","Percent of adults who are not high school graduates, 2019-23","Percent of adults who are high school graduates (or equivalent), 2019-23","Percent of adults completing some college or associate degree, 2019-23","Percent of adults with a bachelor's degree or higher, 2019-23"])


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,mean_squared_error,r2_score




#equal frequency binning 
median = allData["COVID Cases"].median()
labels = ['low','medium','high','really fucking high']
bins = [0,allData["COVID Cases"].quantile(0.30),allData["COVID Cases"].quantile(0.60),allData["COVID Cases"].quantile(0.9),1]

#labels = ['low','medium','high']
#bins = [0,allData["COVID Cases"].quantile(0.33),allData["COVID Cases"].quantile(0.66),1]


allData["COVID Cases"] = pd.cut(allData["COVID Cases"], bins = bins, labels = labels)

allData = allData.dropna()

X = allData.drop(columns = ["COVID Cases","COVID Deaths","Percent Deaths of Cases"])
map_label_to_int = {name: n for n, name in enumerate(labels)}
Y = allData["COVID Cases"].replace(map_label_to_int)

X_train, X_test, y_train, y_test = train_test_split(X,Y,random_state=7,test_size=0.25, shuffle=True,stratify= Y)

decisionTree = DecisionTreeClassifier(min_samples_split=20, random_state=7, max_depth=5)


decisionTree.fit(X_train,y_train)
y_predicted = decisionTree.predict(X_test)
print("Single Tree")
print("Accuracy= ", accuracy_score(y_test,y_predicted))
print("R2 Score = ", r2_score(y_test,y_predicted))
print("Mean Squared = ", mean_squared_error(y_test,y_predicted))

from sklearn.tree import export_graphviz
import subprocess
#https://chrisstrelioff.ws/sandbox/2015/06/08/decision_trees_in_python_with_scikit_learn_and_pandas/
def tree_to_dot(tree, feature_names):
    with open("dt.dot", 'w') as f:
        export_graphviz(tree, out_file=f,
                        feature_names=feature_names)

tree_to_dot(decisionTree, X.columns.tolist())

from sklearn.ensemble import RandomForestRegressor
randomForestReg = RandomForestRegressor(n_estimators= 100, random_state= 7)
randomForestReg.fit(X_train,y_train)
y_predicted = randomForestReg.predict(X_test)
print("Random Forest Regressor")
print("R2 Score = ", r2_score(y_test,y_predicted))
print("Mean Squared = ",mean_squared_error(y_test,y_predicted))


from sklearn.ensemble import RandomForestClassifier
randomForestClass = RandomForestClassifier(n_estimators= 20, random_state= 7)
randomForestClass.fit(X_train,y_train)
y_predicted = randomForestClass.predict(X_test)
print("Random Forest Classifier")
print("Accuracy= ", accuracy_score(y_test,y_predicted))
print("R2 Score = ", r2_score(y_test,y_predicted))
print("Mean Squared = ",mean_squared_error(y_test,y_predicted))

#Optimisation
param_grid = {
    'n_estimators': [25,100,150,250],
    'max_depth': [None,5,10,25],
    'min_samples_split':[2,5,10,20],
    'max_features':[None, 'sqrt','log2']
}


from sklearn.model_selection import GridSearchCV
optimizedRandomTreeReg = RandomForestRegressor(random_state = 7)

grid_search = GridSearchCV(estimator = optimizedRandomTreeReg, param_grid= param_grid,cv=5, n_jobs=-1,verbose=1)
grid_search.fit(X_train,y_train)

best_params = grid_search.best_params_
best_tree = grid_search.best_estimator_

y_predicted = best_tree.predict(X_test)
print("Best Random Forest Regressor")
#print("Accuracy= ", accuracy_score(y_test,y_predicted))
print("R2 Score = ", r2_score(y_test,y_predicted))
print("Mean Squared = ",mean_squared_error(y_test,y_predicted))



optimizedRandomTreeClass = RandomForestClassifier(random_state = 7)

grid_search = GridSearchCV(estimator = optimizedRandomTreeClass, param_grid= param_grid,cv=5, n_jobs=-1,verbose=1)
grid_search.fit(X_train,y_train)

best_params = grid_search.best_params_
best_tree = grid_search.best_estimator_

y_predicted = best_tree.predict(X_test)
print("Best Random Forest Regressor")
print("Accuracy= ", accuracy_score(y_test,y_predicted))
print("R2 Score = ", r2_score(y_test,y_predicted))
print("Mean Squared = ",mean_squared_error(y_test,y_predicted))