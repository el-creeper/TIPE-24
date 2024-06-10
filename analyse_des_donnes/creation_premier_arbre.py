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

def sigma_permut(i):
    """permutation pour remettre les rank dans le bonne ordre
s
        'a'     0       -->     9
        'a+'    1       -->     10
        'a-'    2       -->     8
        'b'     3       -->     6
        'b+'    4       -->     7
        'b-'    5       -->     5
        'c'     6       -->     3
        'c+'    7       -->     4
        'c-'    8       -->     2
        'd'     9       -->     0
        'd+'    10      -->     1
        's'     11      -->     12
        's+'    12      -->     13
        's-'    13      -->     11
        'ss'    14      -->     14
        'u'     15      -->     15
        'x'     16      -->     16

    Args:
        i int: numero de colonnes
    Returns:
        i int: numero permuter
    """
    
    t = [9,10,8,6,7,5,3,4,2,0,1,12,13,11,14,15,16]
    return t[i]

def permut_tab(tab,sigma):
    t = tab.copy()
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            t[sigma(i)][sigma(j)] = tab[i][j]
    return t

def permut_vecteur(tab, sigma):
    t = tab.copy()
    for i in range(len(tab)):
        t[sigma(i)] = tab[i]
    return t
    
    
df = pd.read_csv('analyse_des_donnes/donnes_a_traiter.csv')

X = df.drop("rank",axis=1).copy()

Y = df["rank"].copy()

Y_encoded = pd.get_dummies(Y,"rank")


X_train, X_test, Y_train, Y_test = train_test_split(X,Y_encoded, random_state=42)

for critere in ["gini", "entropy", "log_loss"]:
    clf_dt = DecisionTreeClassifier(criterion = critere,random_state=42)
    clf_dt = clf_dt.fit(X_train,Y_train)

    Y_pred = clf_dt.predict(X_test)

    print("ok?")

    print("hauteur : ",clf_dt.get_depth(),"\nnombre de feuilles  : ",clf_dt.tree_.n_leaves,"\nnombre de noeuds : ",clf_dt.tree_.node_count)

    plt.figure(figsize=(20,15))
    plot_tree(clf_dt,filled = True, rounded = True,proportion = True ,class_names=df["rank"].unique(),feature_names=X.columns, max_depth=1)
    plt.savefig("analyse_des_donnes/premier_arbre"+critere+".svg",format = "svg", dpi=43)
    plt.close()

    plt.figure(figsize=(20,15))
    ax= plt.subplot()
    cm = confusion_matrix(np.asarray(Y_test).argmax(axis=1),np.asarray(Y_pred).argmax(axis=1))
    
    s=0
    for i in range(len(cm)):
        s+=cm[i][i]
    print(s)
    
    s=0
    for l in cm:
        for e in l:
            s+=e
    print(s)
    
    cm = np.round(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], 3)    #on normalise pour avoir des pourcentages
    cm = permut_tab(cm,sigma_permut)




    norm = mcolors.LogNorm(vmin=cm.min()+1e-4, vmax=1)

    masked_cm = np.ma.masked_where(cm == 0, cm)

    # Afficher la heatmap
    sns.heatmap(masked_cm, annot=True, fmt='.3f', ax=ax, norm=norm, cbar_kws={"extend": "min"})

    # Augmenter la taille de la police pour les labels des axes
    ax.set_xlabel('Predicted labels', fontsize=32)
    ax.set_ylabel('True labels', fontsize=32)
    ax.set_title('Confusion Matrix', fontsize=32) 

    # Augmenter la taille de la police pour les tick labels
    name_axis = permut_vecteur(df["rank"].unique(), sigma_permut)
    ax.xaxis.set_ticklabels(name_axis, fontsize=32)
    ax.yaxis.set_ticklabels(name_axis, fontsize=32)

    # Sauvegarder la figure
    plt.savefig("analyse_des_donnes/Confusion_Matrix"+critere+".svg", format='svg', dpi=43)
    plt.close()

print("FINI")