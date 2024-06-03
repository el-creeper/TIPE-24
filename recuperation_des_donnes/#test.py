#test 
#C'est trop bien
import sys
sys.path.append('Comprehension_des_donnees')

from mise_en_forme_des_fichiers import chemin_to_dict, creer_arbre,enregistre_arbre_text



dico = chemin_to_dict(f"Comprehension_des_donnees/Exemple de replay.txt")
arbre = creer_arbre(dico)
string = enregistre_arbre_text(arbre,"test5")


"test"