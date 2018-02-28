from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import subprocess, os, graphviz
import pandas as pd

class Modeler():
    def runCVModel(self,ele, X_train, X_test, y_train, y_test):
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
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    df = pd.read_csv(r"C:\Users\hh769nn\PycharmProjects\Oscar_Prediction\past_historical_data.csv")

    #art_directors_guild_winner_categories
    #writers_guild_winner_categories
    #costume_designers_guild_winner_categories
    #online_film_television_association_winner_categories
    #df['online_film_critics_society_winner_categories_best_film_yes']       = df['online_film_television_association_winner_categories'].str.find("Best Film") > -1
    #df['online_film_critics_society_winner_categories_best_picture_yes']    = df['online_film_television_association_winner_categories'].str.find("Best Picture") > -1
    #people_choice_winner_categories

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

    featureLst = []
    for ele in df.columns:
        if ele.find("yes") > -1:
            featureLst.append(ele)

    #featureLst.append("critic_reviews")
    #featureLst.append("awards_nominations")

    y = df["oscar_best_picture_winner"]
    X = df[featureLst]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=23)
    paramters = {'max_depth': range(3,20)}

    clf = GridSearchCV(RandomForestClassifier(max_depth=25, random_state=0), paramters, n_jobs= 4)
    #paramters = {}
    #clf = GridSearchCV(LogisticRegression(),paramters, n_jobs= 10)

    modelList = [RandomForestClassifier(max_depth=20, random_state=0),LogisticRegression(), DecisionTreeClassifier()]
    #clf = DecisionTreeClassifier(min_samples_split=20, random_state=99)
    #clf = RandomForestClassifier(max_depth=10, random_state=0)
    #clf = LogisticRegression()
    model = Modeler()
    for ele in modelList:
        model.runCVModel(ele,X_train, X_test, y_train, y_test )


'''
    dot_data = export_graphviz(clf, out_file=None,
                             feature_names=featureLst,
                             class_names=df.oscar_best_picture_winner,
                             filled=True, rounded=True,
                             special_characters=True)
    graph = graphviz.Source(dot_data)
'''
