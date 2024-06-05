import os


recup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recup_dir = os.path.join(recup_dir, "stockage_des_donnees")

def parcour_execut(f):
    t = []
    files = os.listdir(recup_dir)
    for dossier in files:
        replay_dir = os.path.join(recup_dir,dossier)
        for replay in os.listdir(replay_dir):
            print(os.listdir(replay_dir))
            replay_fichier = open(replay,"r")
            dict_replay = json.loads(replay_fichier.read())
            replay.close()
            t.append(f(dict_replay))
    return t

def f():
    return 1

print(parcour_execut(f))