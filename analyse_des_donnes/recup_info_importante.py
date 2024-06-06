import os
import json
import csv



recup_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recup_dir = os.path.join(recup_dir, "stockage_des_donnees")

def valider_json(fichier_chemin):
    try:
        with open(fichier_chemin, 'r', encoding='utf-8') as fichier:
            json.load(fichier)
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}",fichier_chemin)
    except Exception as e:
        print(f"Une autre erreur s'est produite : {e}",fichier_chemin)
        

def parcour_execut(f):
    """fonctions qui parcourt tous les repalys et qui renvoie le tableau [f(replay)]
    Args:
        f fun : dict -> object: fonction qui vise à récuperer les informations

    Returns:
        tab: tableau des données récuperer
    """
    t = []
    files = os.listdir(recup_dir)
    for rank in files:
        replay_dir = os.path.join(recup_dir,rank)
        for replay in os.listdir(replay_dir):
            replay_dir = os.path.join(recup_dir, rank, replay)
            valider_json(replay_dir)
            replay_fichier = open(replay_dir,"r")
            dict_replay = json.loads(replay_fichier.read())
            replay_fichier.close()
            t.append(f(dict_replay,rank))
            
            t_f = split_tableau(t)
            
            t_f = [["rank", "nb_frame","moy_apm", "moy_pps", "moy_vs", "apm", "pps", "vs"]]+t_f
    return t_f

def recup_info(dict_replay,rank):
    """recupere les apm, pps, vs moyen et pour chaque partie

    Args:
        dict_replay dict: dictionnaire d'un replay d'une game
        rank float: un floatant represantant un rank

    Returns:
        tab: un tableau qui renvoie les infos de chaque game 
    """
    moy_apm = dict_replay["endcontext"][0]["points"]["secondary"]                                           #float
    moy_pps = dict_replay["endcontext"][0]["points"]["tertiary"]                                            #float
    moy_vs = dict_replay["endcontext"][0]["points"]["extra"]["vs"]                                          #float
    apm = dict_replay["endcontext"][0]["points"]["secondaryAvgTracking"]                                    #tab
    pps = dict_replay["endcontext"][0]["points"]["tertiaryAvgTracking"]                                     #tab
    vs = dict_replay["endcontext"][0]["points"]["extraAvgTracking"]["aggregatestats___vsscore"]             #tab
    
    # recuperation du temps (en frame) des games
    
    time = []
    for game in dict_replay["data"]: #game est un dictionnaire

        time.append(game["replays"][0]["frames"])
        
    #verification des donnees
    
    assert len(time) == len(apm), "time et apm ne sont pas de meme longueur"
    assert len(time) == len(pps), "time et pps ne sont pas de meme longueur"
    assert len(time) == len(vs), "time et vs ne sont pas de meme longueur"
    
    #creation des games
    
    res_inter = [[rank, time[i],moy_apm, moy_pps, moy_vs, apm[i], pps[i], vs[i]] for i in range(len(time))] #parcour pour chaque round

    
    return res_inter


def split_tableau(gros_t):
    """Transforme un tableau de tableau de tableau en tableau de tableau

    Args:
        gros_t tab: un tableau de tableau de tableau

    Returns:
        tab: un tableau de tableau
    """
    nv_t = []
    for petit_t in gros_t:
        for round in petit_t:
            nv_t.append(round)
    return nv_t

def tableau_en_csv(tableau, chemin_fichier):
    """
    Transforme un tableau en fichier CSV.

    Args:
    tableau (list of list): Le tableau à transformer en CSV.
    chemin_fichier (str): Le chemin du fichier CSV à créer.
    """
    try:
        with open(chemin_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.writer(fichier_csv)
            for ligne in tableau:
                writer.writerow(ligne)
        print(f"Fichier CSV créé avec succès : {chemin_fichier}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")
        
        
tableau = parcour_execut(recup_info)     
        
tableau_en_csv(tableau,"analyse_des_donnes/donnes_a_traiter.csv")