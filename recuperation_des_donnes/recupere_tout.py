import json
import requests

def dict_of_page(url):
    url = """https://ch.tetr.io/api/"""+url
    reponse = requests.get(url)
    if reponse.status_code!=200:
        print("Echec de la requete")
    else:
        return(json.loads(reponse.text))

def save_dict_of_page(url,name):
    dict = dict_of_page(url)
    fichier = open("recuperation_des_donnes/"+name,'w')
    with fichier as f:
        f.write(json.dumps(dict,indent=4))
        
save_dict_of_page("users/lists/league/all","all_league")