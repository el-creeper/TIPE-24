import numpy as np

def nb_aleatoire():
    mean = 5
    lower_limit = 4
    upper_limit = 6
    std_dev = 2.595242368834525
    random_number = np.random.normal(mean, std_dev)
    return(random_number)