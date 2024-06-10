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
import seaborn as sns
import matplotlib.colors as mcolors

df = pd.read_csv('mathilde/donnes_de_math.csv')

X = df.drop("Clear",axis=1).copy()

Y = df["Clear"].copy()

Y_encoded = pd.get_dummies(Y,"Clear")


X_train, X_test, Y_train, Y_test = train_test_split(X,Y_encoded, random_state=42)

for critere in ["gini", "entropy", "log_loss"]:
    clf_dt = DecisionTreeClassifier(criterion = critere,random_state=42)
    clf_dt = clf_dt.fit(X_train,Y_train)

    Y_pred = clf_dt.predict(X_test)

    print("ok?")

    print("hauteur : ",clf_dt.get_depth(),"\nnombre de feuilles  : ",clf_dt.tree_.n_leaves,"\nnombre de noeuds : ",clf_dt.tree_.node_count)

    plt.figure(figsize=(20,15))
    plot_tree(clf_dt,filled = True, rounded = True,proportion = True ,class_names=df["Clear"].unique(),feature_names=X.columns, max_depth=1)
    plt.savefig("mathilde/premier_arbre_"+critere+".svg",format = "svg", dpi=43)
    plt.close()

    plt.figure(figsize=(20,15))
    ax= plt.subplot()
    cm = confusion_matrix(np.asarray(Y_test).argmax(axis=1),np.asarray(Y_pred).argmax(axis=1))
    
    s1=0
    for i in range(len(cm)):
        s1+=cm[i][i]

    
    s2=0
    for l in cm:
        for e in l:
            s2+=e
    print('Corect : ', int(s1/s2),"%")
    
    cm = np.round(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], 3)    #on normalise pour avoir des pourcentages




    norm = mcolors.LogNorm(vmin=cm.min()+1e-4, vmax=1)

    masked_cm = np.ma.masked_where(cm == 0, cm)

    # Afficher la heatmap
    sns.heatmap(masked_cm, annot=True, fmt='.3f', ax=ax, norm=norm, cbar_kws={"extend": "min"})

    # Augmenter la taille de la police pour les labels des axes
    ax.set_xlabel('Predicted labels', fontsize=32)
    ax.set_ylabel('True labels', fontsize=32)
    ax.set_title('Confusion Matrix', fontsize=32) 

    # Augmenter la taille de la police pour les tick labels
    name_axis = df["Clear"].unique()
    ax.xaxis.set_ticklabels(name_axis, fontsize=32)
    ax.yaxis.set_ticklabels(name_axis, fontsize=32)

    # Sauvegarder la figure
    plt.savefig("mathilde/Confusion_Matrix_"+critere+".svg", format='svg', dpi=43)
    plt.close()

print("FINI")