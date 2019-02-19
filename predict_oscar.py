from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import subprocess, os
import pandas as pd
import pickle


#model object
class Modeler():
    def runCVModel(self,ele, X_train, X_test, y_train, y_test):
        #no paramater is Logistic Regression, two parameters if not
        if str(ele).startswith("Log"):
            paramters = {}
        else:
            paramters = {'max_depth': range(3, 20)}
        clf = GridSearchCV(ele,paramters, n_jobs= 10)
        clf.fit(X_train, y_train)
        tree_model = clf.best_estimator_
        predicted = tree_model.predict(X_test)
         # summarize the fit of the model
        print(metrics.classification_report(y_test, predicted))
        print(metrics.confusion_matrix(y_test, predicted))
        print(accuracy_score(y_test, predicted))

if __name__ == '__main__':
    #os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    df = pd.read_csv("past_historical_data.csv")

    #past award data read as "Best Film; Best Actress" which needs to be converted into discrete categories
    df['bafta_winner_categories_yes']                                       = (df['bafta_winner_categories'].str.find("Best Film") > -1) & (df['bafta_winner_categories'].str.find("Best Film not") <= -1)
    df['screen_actors_guild_winner_categories_yes']                         = df['screen_actors_guild_winner_categories'].str.find("Cast") > -1
    df['critics_choice_winner_categories_yes']                              = df['critics_choice_winner_categories'].str.find("Best Picture") > -1
    df['directors_guild_winner_categories_yes']                             = df['directors_guild_winner_categories'].str.find("Directorial") > -1
    df['producers_guild_winner_categories_yes']                             = df['producers_guild_winner_categories'].str.find("of Theatrical Motion") > -1
    df['london_critics_circle_film_winner_categories_yes']                  = df['online_film_television_association_winner_categories'].str.find("Film of the Year") > -1
    df['american_cinema_editors_winner_categories_yes']                     = df['american_cinema_editors_winner_categories'].str.find("Film") > -1
    df['hollywood_film_winner_categories_yes']                              = df['hollywood_film_winner_categories'].str.find("Film of the Year") > -1
    df['austin_film_critics_association_winner_categories_yes']             = df['austin_film_critics_association_winner_categories'].str.find("Best Film") > -1
    df['denver_film_critics_society_winner_categories']                     = df['denver_film_critics_society_winner_categories'].str.find("Best Picture") > -1
    df['boston_society_of_film_critics_winner_categories_yes']              = df['boston_society_of_film_critics_winner_categories'].str.find("Best Film") > -1
    df['new_york_film_critics_circle_winner_categories_yes']                = df['new_york_film_critics_circle_winner_categories'].str.find("Best Film") > -1
    df['los_angeles_film_critics_association_winner_categories_yes']        = df['los_angeles_film_critics_association_winner_categories'].str.find("Best Picture") > -1

    #using only the newly created discrete award show data as features for our models
    featureLst = []
    for ele in df.columns:
        if ele.find("yes") > -1:
            featureLst.append(ele)


    #setting the x and y vectors       
    y = df["oscar_best_picture_winner"]
    X = df[featureLst]

    #spliting the data set into traing and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=23)
    
    #creating the list of models to test, and for looping thru the list of models thru modeler object cross validation
    modelList = [RandomForestClassifier(max_depth=20, random_state=0),LogisticRegression(), DecisionTreeClassifier()]
    model = Modeler()
    for ele in modelList:
        model.runCVModel(ele,X_train, X_test, y_train, y_test)
        filename = "models/"+str(ele.__class__).split(".")[-1].split("'")[0]+".sav"
        pickle.dump(model, open(filename, 'wb'))



