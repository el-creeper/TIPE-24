import json
import requests
import random

N = 50 #taille de l'echantion (pour un rank)

fichier = open("recuperation_des_donnes/all_league",'r')
print("ok")
dict = (json.loads(fichier.read()))["data"]["users"]

d_rank = {}

# Répartit les joueurs dans un dictionnaire avec comme clé les rank

for users in dict:
    if users["league"]["rank"] in d_rank:
        d_rank[users["league"]["rank"]].append(users["username"])
    else:
        d_rank[users["league"]["rank"]]=[users["username"]]
        
#print la taille du nombre de joueurs        

d_taille = {}
for rank in d_rank:
    d_taille[rank] = len(d_rank[rank])
    
print(d_taille)
        
# créer l'échantion
        
d_sample ={}
        
for rank in d_rank:
    if rank != "z":
        N_rank = min(N,d_taille[rank])
        d_sample[rank] = random.sample(d_rank[rank], N_rank)

fichier = open("recuperation_des_donnes/ids_echantillons",'w')
with fichier as f:
    f.write(json.dumps(d_sample,indent=4))