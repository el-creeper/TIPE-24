import json

sub_d = {}
fichier = open("recuperation_des_donnes/ids_echantillons",'r')
dict = json.loads(fichier.read())

for rank in dict:
    c=0
    if rank not in sub_d:
        sub_d[rank] = []
        for i_id in range(0,len(dict[rank]),10):
            sub_d[rank].append(dict[rank][i_id:min(i_id+10,len(dict[rank]))])

def mise_en_forme(tableau):
    text = "user" + tableau[0]+" league saveas \"%Y-%m-%d %H-%M 40L %T.ttrm\"" 
    for user in tableau:
        if not user == tableau[0]:
            text += "\nalso user" + user+" league saveas \"%Y-%m-%d %H-%M 40L %T.ttrm\""
    return text

print(mise_en_forme(sub_d["x"][0]))