import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import datasets
from sklearn import tree


df = pd.read_csv('analyse_des_donnes/donnes_a_traiter.csv')

X = df.drop("rank",axis=1).copy()

Y = df["rank"].copy()

Y_encoded = pd.get_dummies(Y,"rank")


X_train, X_test, Y_train, Y_test = train_test_split(X,Y_encoded, random_state=42)


clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train,Y_train)

print("ok?")

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(clf_dt, 
                   filled=True)
plt.plot(fig)


print("FINI")