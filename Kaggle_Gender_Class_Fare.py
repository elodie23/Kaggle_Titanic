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


# MODEL 2 - GENDER (Male/Female), CLASS (1,2,3), FARE (4 segments)

# 1. Créer une table avec 0/1 pour chaque valeur de variable explicative
# 2. Indiquer le taux de survie pour chaque combinaison (gender, class, fare)

fare_ceiling = 40
data[ data[0::,9].astype(np.float) >= fare_ceiling, 9 ] = fare_ceiling - 1.0
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

number_of_classes = len(np.unique(data[0::,2]))

survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in xrange(number_of_classes):       
     for j in xrange(number_of_price_brackets): 
         women_only_stats = data[(data[0::,4] == "female")&(data[0::,2].astype(np.float)== i+1)&(data[0:,9].astype(np.float)>= j*fare_bracket_size)&(data[0:,9].astype(np.float)<(j+1)*fare_bracket_size), 1]  
         men_only_stats = data[(data[0::,4] != "female")&(data[0::,2].astype(np.float)== i+1)&(data[0:,9].astype(np.float)>= j*fare_bracket_size)&(data[0:,9].astype(np.float)<(j+1)*fare_bracket_size), 1]
         survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float)) 
         survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

survival_table[ survival_table != survival_table ] = 0.
print survival_table

# 3. Faire un modèle simple 0/1 sur cette base et l'appliquer à la base test

survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1 
print survival_table

test_file = open('C:/Big Data - Kaggle/test.csv','rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()

predictions_file = open("C:/Big Data - Kaggle/genderclassmodel.csv", "wb")
p = csv.writer(predictions_file)
p.writerow(["PassengerId", "Survived"])

for row in test_file_object:   
    for j in xrange(number_of_price_brackets):  
       try:       
           row[8] = float(row[8]) 
       except:
           bin_fare = 3 - float(row[1])
           break
       if row[8] > fare_ceiling:
           bin_fare = number_of_price_brackets-1
           break
       if row[8] >= j * fare_bracket_size and row[8] < (j+1) * fare_bracket_size: 
           bin_fare = j 
           break
    if row[3] == 'female':   
       p.writerow([row[0], "%d" % int(survival_table[0, float(row[1])-1, bin_fare])])
    else:                                     
       p.writerow([row[0], "%d" % int(survival_table[1, float(row[1])-1, bin_fare])])

test_file.close()
predictions_file.close()