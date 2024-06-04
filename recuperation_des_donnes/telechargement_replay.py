import subprocess
import os
import re
import shutil
import pyautogui
import time
import json



# Obtenir le chemin absolu du répertoire contenant le script Python
script_dir = os.path.dirname(os.path.abspath(__file__))

# Nom de l'exécutable à lancer
exe_name = "inoue.exe"

exe_path = os.path.join("inoue", exe_name) 
print(exe_path)

def requete():
    try:
        process = subprocess.Popen(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        time.sleep(1)
        pyautogui.press("a")
        stdout, stderr = process.communicate()

        print("Sortie standard :", stdout.decode())
        print("Erreur standard :", stderr.decode())
        
        print("L'exécutable s'est terminé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"L'exécution de l'exécutable a échoué : {e}")
    except FileNotFoundError:
        print(f"L'exécutable {exe_name} est introuvable.")


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
        print(f"Fichier déplacé de {source_path} à {dest_path}")
    except Exception as e:
        print(f"Erreur lors du déplacement du fichier : {e}")
    
    
def move():
    files = os.listdir()
    for file in files:
        res = re.match(r"\d{2}-\d{2}-\d{4} \d{2}-\d{2} league .ttrm",file)
        if res != None: 
            path = (res.group(0))
            move_file(path, "stockage_des_donnees") 

sub_d = {}
fichier = open("recuperation_des_donnes/ids_echantillons",'r')
dict = json.loads(fichier.read())

for rank in dict:
    c=0
    if rank not in sub_d:
        sub_d[rank] = []
        for i_id in range(0,dict[rank],10):
            sub_d[rank].append(dict[rank][i_id:min(i_id+10,len(dict[rank]))])
            
def mise_en_forme(tableau):
    text = "user" + tableau[0]+" league saveas \"%Y-%m-%d %H-%M 40L %T.ttrm\"" 
    for user in tableau:
        if not user == tableau[0]:
            text += "\n user" + user+" league saveas \"%Y-%m-%d %H-%M 40L %T.ttrm\""
    return text

for rank in sub_d:
    inoue = open("inoue.txt","w")
    for t in sub_d[rank]:
        with inoue as f:
            f.write(mise_en_forme(t))
            temps = time.time()
            requete()
            move()
            if time.time()-temps >0:
                time.sleep(time.time()-temps)
                