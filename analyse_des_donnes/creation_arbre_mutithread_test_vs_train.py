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
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def sigma_permut(i):
    """permutation pour remettre les rank dans le bonne ordre"""
    t = [9,10,8,6,7,5,3,4,2,0,1,12,13,11,14,15,16]
    return t[i]

def permut_tab(tab, sigma):
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

def fit_decision_tree(alpha):
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=alpha)
    clf_dt.fit(X_train, Y_train)
    train_score = clf_dt.score(X_train, Y_train)
    test_score = clf_dt.score(X_test, Y_test)
    return clf_dt, train_score, test_score

df = pd.read_csv('analyse_des_donnes/donnes_a_traiter.csv')

X = df.drop("rank", axis=1).copy()
Y = df["rank"].copy()
Y_encoded = pd.get_dummies(Y, "rank")

X_train, X_test, Y_train, Y_test = train_test_split(X, Y_encoded, random_state=42)

clf_dt = DecisionTreeClassifier(random_state=42)
clf_dt = clf_dt.fit(X_train, Y_train)

Y_pred = clf_dt.predict(X_test)

path = clf_dt.cost_complexity_pruning_path(X_train, Y_train)

alphas = path.ccp_alphas
alphas = alphas[:-1]

clf_dts = []
train_scores = []
test_scores = []

print(len(alphas))

with ThreadPoolExecutor() as executor:
    future_to_alpha = {executor.submit(fit_decision_tree, alpha): alpha for alpha in alphas}
    
    for future in tqdm(as_completed(future_to_alpha), total=len(alphas), desc="Processing", mininterval=30):
        alpha = future_to_alpha[future]
        try:
            clf_dt, train_score, test_score = future.result()
            clf_dts.append(clf_dt)
            train_scores.append(train_score)
            test_scores.append(test_score)
        except Exception as exc:
            print(f'Alpha {alpha} generated an exception: {exc}')

t_data = [[alphas[i], train_scores[i], test_scores[i]] for i in range(len(alphas))]

with open("analyse_des_donnes/scores.txt", 'w') as fichier:
    fichier.write(str(t_data))

print(max(t_data))
print("ok")

fig, ax = plt.subplots()
ax.set_xlabel("alpha")
ax.set_ylabel("Précision")
ax.set_title("Précision en fonction de alpha pour l'ensemble entrainement et test")
ax.plot(alphas, train_scores, marker='o', label="train", drawstyle="steps-post")
ax.plot(alphas, test_scores, marker='o', label="test", drawstyle="steps-post")
ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()
plt.savefig("analyse_des_donnes/graphe_alpha_test_vs_train.svg", format="svg")
plt.show()
