import subprocess
import os
import re
import shutil
import pyautogui
import time
import json
import numpy as np

print("programme lancer")

k=1


# Obtenir le chemin absolu du répertoire contenant le script Python
script_dir = os.path.dirname(os.path.abspath(__file__))

# Nom de l'exécutable à lancer
exe_name = "inoue.exe"

exe_path = os.path.join("inoue", exe_name) 
print(exe_path)

def requete(exe_path):
    try:
        # Lancer l'exécutable
        process = subprocess.Popen(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre que l'exécutable ait fini de s'exécuter
        process.wait()
        
        # Attendre un court instant pour s'assurer que le programme est prêt pour l'entrée clavier
        time.sleep(1)
        
        # Envoyer une touche au programme
        pyautogui.press("a")
        
        # Attendre encore un peu pour s'assurer que la touche a été reçue et traitée
        time.sleep(1)
        
        # Vérifier si le processus est toujours en cours et le terminer s'il ne l'est pas
        if process.poll() is None:
            process.terminate()
            process.wait()
        
        # Lire la sortie du programme
        stdout, stderr = process.communicate()

    except subprocess.CalledProcessError as e:
        print(f"L'exécution de l'exécutable a échoué : {e}")
    except FileNotFoundError:
        print(f"L'exécutable {exe_path} est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def move_file(source_path, dest_dir):
    # Vérifier si le fichier source existe
    if not os.path.isfile(source_path):
        print(f"Le fichier source {source_path} n'existe pas.")
        return

    # Créer le répertoire de destination s'il n'existe pas
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Définir le chemin de destination complet
    dest_path = os.path.join(dest_dir, os.path.basename(source_path))

    try:
        # Déplacer le fichier
        shutil.move(source_path, dest_path)

    except Exception as e:
        print(f"Erreur lors du déplacement du fichier : {e}")
    
    
def move(rank):
    # Obtenir le chemin du répertoire du script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest_dir = os.path.join(base_dir, "stockage_des_donnees", rank)
    # Obtenir la liste des fichiers dans le répertoire courant du script
    files = os.listdir(base_dir)
    files = os.listdir()
    for file in files:
        res = re.match(r'^[A-Z0-9-_]+ vs [A-Z0-9-_]+ \d{4}-\d{2}-\d{2} \d{2}-\d{2} league (\d{1,2}\'\d{2}\.\d{3})?\.ttrm$',file)
        if res != None:
            path = os.path.join(base_dir, res.group(0))
            move_file(path, dest_dir)

sub_d = {}
fichier = open("recuperation_des_donnes/ids_echantillons",'r')
dict = json.loads(fichier.read())

for rank in dict:
    c=0
    if rank not in sub_d:
        sub_d[rank] = []
        for i_id in range(0,len(dict[rank]),k):
            sub_d[rank].append(dict[rank][i_id:min(i_id+k,len(dict[rank]))])
            
def mise_en_forme(tableau):
    text = "user " + tableau[0]+" league saveas \"%U vs %O %Y-%m-%d %H-%M league %T.ttrm\"" 
    for user in tableau:
        if not user == tableau[0]:
            text += "\nalso user " + user+" league saveas \"%U vs %O %Y-%m-%d %H-%M league %T.ttrm\""
    return text


def nb_aleatoire():
    mean = 5
    lower_limit = 4
    upper_limit = 6
    std_dev = 2.595242368834525
    random_number = np.random.normal(mean, std_dev)
    return(random_number)


for rank in sub_d:
    ct = 0
    for t in sub_d[rank]:
        ct += 1
        inoue = open("inoue.txt","w")
        inoue.write(mise_en_forme(t))
        inoue.close()
        temps = time.time()
        requete(exe_path)
        move(rank)
        time.sleep(2*max(nb_aleatoire(),0))
        print(ct)
        
print("FINI")
                