# -*- coding: utf-8 -*-
"""
Created on Sat Apr 02 15:10:00 2016

@author: E-FOURGOUS
"""

# Import des packages
import csv as csv 
import numpy as np

# Lire le fichier csv
csv_file_object = csv.reader(open('C:/Big Data - Kaggle/train.csv', 'rb'))
header = csv_file_object.next() 
 
# Stocker la base de données dans l'objet data 
data=[]
for row in csv_file_object: 
    data.append(row) 
data = np.array(data)

# Décompte Nb passagers et survivants
number_passengers = np.size(data[0::,1].astype(np.float))
number_survived = np.sum(data[0::,1].astype(np.float))
proportion_survivors = number_survived / number_passengers
print ' '
print 'Total Stats:'
print 'Nb passengers=', number_passengers
print 'Nb survivors=', number_survived
print 'Survival rate=', proportion_survivors

# Décompte pour femmes et hommes
#  1). Créer une colonne FAUX/VRAI 
women_only_stats = data[0::,4] == "female"
men_only_stats = data[0::,4] != "female"

#  2). Remplacer FAUX/VRAI par 0/1
women_onboard = data[women_only_stats,1].astype(np.float)     
men_onboard = data[men_only_stats,1].astype(np.float)

#  3). Nb d'hommes et femmes à bord
Nb_women=np.size(women_onboard) 
Nb_men=np.size(men_onboard) 

#  4). Nb de survivants hommes et femmes
Nb_survived_women=np.sum(women_onboard) 
Nb_survived_men=np.sum(men_onboard)

#  5). Taux de survie hommes et femmes
Survival_women=Nb_survived_women/Nb_women  
Survival_men=Nb_survived_men/Nb_men

print ' '
print 'Stats Female:'
print 'Nb Female=', Nb_women
print 'Nb Survivors Female=', Nb_survived_women
print 'Survival rate Female=', Survival_women

print ' '
print 'Stats Male:'
print 'Nb Male=', Nb_men
print 'Nb survivors Male=', Nb_survived_men
print 'Survival rate Male=', Survival_men


# MODEL 1 - GENDER ONLY

#  Il faut ouvrir 1 objet Python pour lire un fichier et 1 autre pour écrire
test_file = open('C:/Big Data - Kaggle/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

prediction_file = open("C:/Big Data - Kaggle/genderbasedmodel.csv", "wb")
prediction_file_object = csv.writer(prediction_file)

#  Survie si femme, décès si homme
prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object: 
    if row[3] == 'female':
        prediction_file_object.writerow([row[0],'1'])    
    else:
        prediction_file_object.writerow([row[0],'0'])    

test_file.close()
prediction_file.close()