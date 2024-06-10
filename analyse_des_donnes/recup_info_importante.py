import os
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

recup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recup_dir = os.path.join(recup_dir, "stockage_des_donnees")

def valider_json(fichier_chemin):
    try:
        with open(fichier_chemin, 'r', encoding='utf-8') as fichier:
            json.load(fichier)
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}", fichier_chemin)
    except Exception as e:
        print(f"Une autre erreur s'est produite : {e}", fichier_chemin)

def recup_info(dict_replay, rank):
    """Recupere les apm, pps moyen et pour chaque partie"""
    moy_apm = dict_replay["endcontext"][0]["points"]["secondary"]  # float
    moy_pps = dict_replay["endcontext"][0]["points"]["tertiary"]   # float
    apm = dict_replay["endcontext"][0]["points"]["secondaryAvgTracking"]  # tab
    pps = dict_replay["endcontext"][0]["points"]["tertiaryAvgTracking"]   # tab

    # Recuperation du temps (en frame) des games
    time = []
    for game in dict_replay["data"]:  # game est un dictionnaire
        time.append(game["replays"][0]["frames"])

    # Verification des donnees
    assert len(time) == len(apm), "time et apm ne sont pas de meme longueur"
    assert len(time) == len(pps), "time et pps ne sont pas de meme longueur"

    # Creation des games
    res_inter = [[rank, time[i], moy_apm, moy_pps, apm[i], pps[i], None] for i in range(len(time))]  # parcour pour chaque round

    return res_inter

def process_replay(replay_dir, rank):
    valider_json(replay_dir)
    with open(replay_dir, "r", encoding='utf-8') as replay_fichier:
        dict_replay = json.load(replay_fichier)
    return recup_info(dict_replay, rank)

def parcour_execut(f):
    """Parcourt tous les replays et renvoie le tableau [f(replay)]"""
    t = []
    files = os.listdir(recup_dir)
    all_replays = [(os.path.join(recup_dir, rank, replay), rank) for rank in files for replay in os.listdir(os.path.join(recup_dir, rank))]

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_replay, replay_dir, rank): (replay_dir, rank) for replay_dir, rank in all_replays}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Replays"):
            try:
                result = future.result()
                if isinstance(result, list):
                    t.extend(result)
            except Exception as e:
                replay_dir, rank = futures[future]
                print(f"Erreur de traitement du fichier {replay_dir} : {e}")

    t_f = split_tableau(t)
    t_f = [["rank", "nb_frame", "moy_apm", "moy_pps", "apm", "pps", "vs"]] + t_f
    return t_f

def split_tableau(gros_t):
    """Transforme un tableau de tableau de tableau en tableau de tableau"""
    nv_t = []
    for petit_t in gros_t:
        if isinstance(petit_t, list):
            for round in petit_t:
                nv_t.append(round)
    return nv_t

def tableau_en_csv(tableau, chemin_fichier):
    """Transforme un tableau en fichier CSV."""
    try:
        with open(chemin_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            for ligne in tableau:
                if isinstance(ligne, list):
                    writer.writerow(ligne)
        print(f"Fichier CSV créé avec succès : {chemin_fichier}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")

tableau = parcour_execut(recup_info)

# Ajout d'une impression pour vérifier le contenu de `tableau`
print(tableau)

tableau_en_csv(tableau, "analyse_des_donnes/donnes_a_traiter_sans_vs.csv")
