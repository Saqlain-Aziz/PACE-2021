from collections import defaultdict
import sys
import signal
from typing import OrderedDict
import copy

#https://www.optil.io/optilion/help/signals#python3
class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True

killer = Killer()

# Algorithme : https://www.lamsade.dauphine.fr/~sikora/ens/graphes/projet2021/vip.pdf

# On recupere le nombre de sommets et d'aretes
p, cep, n, m = input().split()
n = int(n)
m = int(m)

# Creation de la liste d'adjacence
# Creation d'une liste contenant toutes les aretes donnees en entree
adj_list = defaultdict(list)
aretes = []
for i in range(m):
    u, v = map(int, input().split())
    aretes.append((u,v))
    adj_list[u].append(v)
    adj_list[v].append(u)

# creation d'un dictionnaire pour stocker les cliques du graphe
cliques = defaultdict(list)
# initialisation de la premiere clique contenant le sommet 1
cliques[1].append(1)

# fonction qui retourne e (de la formule de l'algorithme) pour un sommet
def getE(sommet):
  return len(adj_list[sommet])

# fonction qui retourne e' (de la formule de l'algorithme) pour un sommet dans une clique donnee
def getEPrime(sommet, clique):
  tmp = 0
  for i in adj_list[sommet]:
    if i in clique:
      tmp += 1
  return tmp

# dictionnaire qui stocke les couts (de la formule de l'algorithme)
tmpCout = {}
cliques_copy = copy.copy(cliques) # copie du dictionnaire clique (couteux en espace mais necessaire sinon erreur l.59)

# stockage des cliques du graphe selon la formule de l'algorithme
for i in range(2, len(adj_list)+1):
  for j in cliques_copy:
    X = len(cliques[j])
    ePrime = getEPrime(i, cliques[j])
    e = getE(i)
    cout = (X - ePrime) + (e - ePrime)
    tmpCout[i] = e
    tmpCout[j] = cout
    coutMin = min(tmpCout, key=tmpCout.get)
    cliques[coutMin].append(i)

# enregistrer les aretes a ajouter / retirer

aretesModif = [] # aretes a ajouter
tmpAretes = [] # elle va stocker toutes les aretes entre les sommets d'une clique

# dans une clique ajouter ceux qui manquent dans aretesModif
for i in cliques:
  for j in cliques[i]:
    for k in cliques[i]:
      if j!=k:
        if ((j,k) not in aretes) and ((k,j) not in aretes):
          if ((j,k) not in aretesModif) and ((k,j) not in aretesModif):
            aretesModif.append((j,k))
        else:
          if((j,k) not in tmpAretes):
            tmpAretes.append((j,k))
          elif((k,j) not in tmpAretes):
            tmpAretes.append((k,j))

aretesSup=[] # aretes a supprimer

for i in range (0, m):
  if aretes[i] not in tmpAretes: # si on passe ce if, l'arete est forcement une arete ayant ses extremites dans deux cliques differentes donc a supprimer
    aretesSup.append(aretes[i])

# affichage des aretes modifiees

for modif in aretesModif:
  print(modif[0], modif[1]) # affichage des aretes a ajouter

for modif in aretesSup:
  print(modif[0], modif[1]) # affichage des aretes a supprimer

#demo of capturing SIGTERM
#to see how it works, run:
#timeout 1 python3 main.py < instance.gr
#exit_now is True after 1 second (in the benchmark, it will be after 10 minutes)
#while True:
    #if killer.exit_now:
      #break