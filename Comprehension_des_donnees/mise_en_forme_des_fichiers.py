#imporation des biliotheques 
import os
from anytree import AnyNode, Node, RenderTree
import json
from graphviz import Digraph, Source
from anytree.dotexport import RenderTreeGraph, DotExporter

#Fonction importante
'''
  chemin_to_dict : fichier venant d'une requete json -> dictionaire lisible
  creer_arbre : Creer l arbre avec le dictionnaire
  enregistre_arbre_text : transformer l arbre en fichier texte
  copier_arbre_profondeur_max : copie l arbre jusqu a une certaine profondeur
  '''


#Fonction rapide

def modifieur(text):
  """Permet d'avoir une copie du texte avec les bonnes indentations
  

  :param text: text du fichier a transformer, defaults to text
  :type text: str, optional
  """
  text_mod = ""
  compteur = 0
  for e in text:
      if e == ',':
          text_mod+=',\n'+'\t'*compteur
      elif e == '{':
          compteur += 1
          text_mod+='\n' +  '\t'*compteur + '{'
      elif e == '}':
          compteur -= 1
          text_mod+='\n' +  '\t'*compteur + '}'
      else:
          text_mod+=e

          chemin2 = 'Exemple de replay_modif.txt'
  fichier = open("Comprehension des donnees/"+chemin2,'x')
  with fichier as f:
      f.write(text_mod)

#Mise en forme de la requete

def chemin_to_dict(chemin):
  """transforme un fichier d une requete json en dictionaire 

  :param chemin: chemin du fichier
  :type chemin: str
  :return: renvoie le dictionnaire de la requete json
  :rtype: dict
  """
  fichier = open(chemin,'r')
  text = fichier.read()
  dictionnaire = json.loads(text)
  return dictionnaire

def text_json_to_dict(text):
  """Transformer un text d une requete json en dictionaiire 
  
  :param text: text contenant le reponse json
  :type text: str
  :return: renvoie le dictionnaire de la requete json
  :rtype: dict
  """
  dictionnaire = json.loads(text)
  return dictionnaire

#Parcourt des données
def creer_arbre(d):
  racine = AnyNode(name = "fichier")
  parcour_dict(d,racine)
  return racine 

def parcour_dict(d,predecesseur):
  """Permet de parcourir un dictionnaire de manière récursive pour créer l'arbre.

    :param d: Dictionnaire à parcourir.
    :type d: dict
    :param predecesseur: Pere du dictionnaire dans l'arbre.
    :type predecesseur: AnyNode, optional
  """
  for cle in d :
    node = AnyNode(name = cle, parent = predecesseur)
    if type(d[cle]) == dict:
      parcour_dict(d[cle],node)
    elif type(d[cle]) == list:
      parcour_tab(d[cle],node)
    else:
      feuille = AnyNode(name = d[cle],parent = node)

def parcour_tab(t,predecesseur):
  """Permet de parcourir une liste de manière récursive pour créer l'arbre.

  :param t: Liste à parcourir.
  :type t: list
  :param predecesseur: pere de la liste dans l'arbre.
  :type predecesseur:  AnyNode
  """

  for i in range(len(t)) :
    node = AnyNode(name = i, parent = predecesseur)
    if type(t[i]) == dict:
      parcour_dict(t[i],node)
    elif type(t[i]) == list:
      parcour_tab(t[i],node)
    else:
      feuille = AnyNode(name = t[i],parent = node)

#Enregistrement des donnees
def enregistre_arbre_string(root):
  string = ""
  for pre, _, node in RenderTree(root):
    string +="%s%s\n" % (pre, node.name)
  return string

def enregistre_arbre_text(root, nom_fichier, repertoire="."):
  """
    Enregistre la structure d'un arbre dans un fichier texte.

    :param root: Nœud racine de l'arbre à enregistrer.
    :type root: anytree.node.anynode.AnyNode
    :param nom_fichier: Nom du fichier dans lequel enregistrer le texte
    :type nom_fichier: str
    :param repertoire: Répertoire dans lequel enregistrer le texte
    :type repertoire: str
  """
  chemin_fichier = os.path.join(repertoire, nom_fichier + ".txt")
  with open(chemin_fichier, "w", encoding="utf-8") as file:
    for pre, _, node in RenderTree(root):
      file.write("%s%s\n" % (pre, node.name))

def enregistre_arbre_dot(root, nom_fichier, repertoire):
  """
    Enregistre la structure d'un arbre dans un fichier au format DOT.

    :param root: Nœud racine de l'arbre à enregistrer.
    :type root: anytree.node.anynode.AnyNode
    :param nom_fichier: Nom du fichier dans lequel enregistrer le format DOT, par défaut "arborescence de la structure de replay".
    :type nom_fichier: str, optional
    :param repertoire: Répertoire dans lequel enregistrer le fichier DOT, par défaut "Compréhension des données".
    :type repertoire: str, optional
    """
  chemin_fichier = f"{repertoire}/{nom_fichier}.dot"
  DotExporter(root).to_dotfile(chemin_fichier)



def enregistre_arbre_image(root, nom_fichier="arborescence de la structure de replay", repertoire="Comprehension des donnees"):
  """
  (Ne crash pas mais pas sur que ca marche)
    Enregistre la structure d'un arbre au format image (PNG) à partir d'un fichier DOT.

    :param root: Nœud racine de l'arbre à enregistrer.
    :type root: anytree.node.anynode.AnyNode
    :param nom_fichier: Nom du fichier dans lequel enregistrer le format DOT, par défaut "arborescence de la structure de replay".
    :type nom_fichier: str, optional
    :param repertoire: Répertoire dans lequel enregistrer le fichier DOT et l'image, par défaut "Compréhension des données".
    :type repertoire: str, optional
    """
  chemin_fichier = f"{repertoire}/{nom_fichier}.dot"
  image_path = "arborescence de la structure de replay.png"
  Source.from_file(chemin_fichier).render(image_path, format="png", cleanup=True)

#Copie partiel de l'arbre

def copier_arbre_profondeur_max(arbre, n):
  """
  Copie un arbre en ne conservant que les nœuds de profondeur inférieure ou égale à n.

  :param arbre: Nœud racine de l'arbre à copier.
  :type arbre: anytree.node.anynode.AnyNode
  :param n: Profondeur maximale à conserver.
  :type n: int
  :return: Nouveau nœud racine de l'arbre copié.
  :rtype: anytree.node.anynode.AnyNode
  """
  def copier_noeud(original, parent=None, profondeur=0):
    if profondeur > n:
      return None

    copie = AnyNode(name=original.name, parent=parent)
    for enfant in original.children:
      copier_noeud(enfant, parent=copie, profondeur=profondeur + 1)

  arbre_copie = AnyNode(name=arbre.name)
  for enfant in arbre.children:
    copier_noeud(enfant, parent=arbre_copie, profondeur=1)

  return arbre_copie
  
