fichier = open("analyse_des_donnes/scores.txt")
t_fichier = fichier.read()
t_fichier = t_fichier.split("]]")

print(len(t_fichier))
print(type(t_fichier))
print(t_fichier)

#tab_fichier = [tab(t_fichier[0]),tab(t)]
