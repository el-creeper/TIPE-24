import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def sigma_permut(i):
    """Permutation pour remettre les rank dans le bonne ordre."""
    t = [9, 10, 8, 6, 7, 5, 3, 4, 2, 0, 1, 12, 13, 11, 14, 15, 16]
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

def cross_val_score_alpha(alpha):
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=alpha)
    scores = cross_val_score(clf_dt, X_train, Y_train, cv=5)
    return alpha, np.mean(scores), np.std(scores)

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

alphas_loop_values = []

print(len(alphas))

with ThreadPoolExecutor() as executor:
    future_to_alpha = {executor.submit(cross_val_score_alpha, alpha): alpha for alpha in alphas}
    
    for future in tqdm(as_completed(future_to_alpha), total=len(alphas), desc="Processing", mininterval=30):
        try:
            alpha, mean_score, std_score = future.result()
            alphas_loop_values.append({"alpha": alpha, "mean_accuracy": mean_score, "std": std_score})
        except Exception as exc:
            alpha = future_to_alpha[future]
            print(f'Alpha {alpha} generated an exception: {exc}')

alpha_result = pd.DataFrame(alphas_loop_values)

alpha_result.plot(
    x='alpha',
    y='mean_accuracy',
    yerr='std',
    marker='o',
    linestyle=''  # This disables the lines between points
)
plt.xlabel('Alpha')
plt.ylabel('Mean Accuracy')
plt.title('Mean Accuracy vs Alpha with Error Bars')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig("analyse_des_donnes/graphe_alpha.svg", format="svg")
plt.show()
