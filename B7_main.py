import pandas as pd

def lire_fichier(fichier):
    file = open(fichier, "r")
    table = file.readlines()
    copie = []
    for item in table:    # item est une copie des elements de la table, donc tous les changements fait n'affecterons pas table. C'est dû à l'utilisation de la boucle for i in
        copie.append(item.strip())  # c'est pourquoi on stock cela dans un nouveau tableau
    table = copie
    return table

def valeur_neg(table):    # table est une liste  de strings récupérer par la lecture du fichier , retourne un booléen
    dur = []
    for i in range(len(table)):
        duree = ""  # p
        partie = table[i].split()
        duree += partie[1]
        dur.append(duree)

    for duration in dur:
        if '-' in duration:

            print("Il y a une durée négative")
            return True

    print("Il n'y a pas de durées négatives")
    return False

def constr_tabc(table):    # retourne une matrice 2D
    #On construit le tableau des contraintes
    mat=[]
    for i in range(len(table)):

        # Remplir la matrice
        ligne = []  # p
        tache = ""  # p
        duree = ""  # p
        contraintes = ""

        partie = table[i].split()
        tache += partie[0]
        duree+=partie[1]


        if len(partie[2:]) ==0 :
            contraintes+="a"
        else:
            for j in  range(len(partie[2:])):
                if partie[2:][-1] == partie[2:][j]:
                    contraintes+= partie[2:][j]
                else:
                    contraintes += partie[2:][j] + " "
        ligne.append(tache)
        ligne.append(duree)
        ligne.append(contraintes)
        mat.append(ligne)

    # Création deux de listes afin de comparer les taches et les contraintes pour ainsi trouver les points terminaux

    cc= []
    t = []
    for j in range(len(mat)):
        t.append(mat[j][0])
        cc.append(mat[j][2])

        # Liste contraintes

    cssdb = []


    #Permet d'avoir une liste 1d des contraintes
    for i in range(len(cc)):
        if len(cc[i])>1:
            r = cc[i].split()
            for j in r:
                if cc[i] != 'a':
                    cssdb.append(j)
        else:
            if cc[i]!= 'a':
                cssdb.append(cc[i])


    #Permet de supprimer les doublons
    cssdbb = list(set(cssdb))

    #comparaison pour avoir les point terminaux
    endpoint = []
    for i in t:
        if i not in  cssdbb:
            endpoint.append(i)
    endpoint = ' '.join(endpoint)

    # on ajoute alpha,omega
    alpha= ["a","",""]
    omega = ["o","",endpoint]

    mat.insert(0,alpha)
    mat.append(omega)
    return mat

def affichage_tabc(tabc):  #    entré : matrice  , retourne une dataFrame
    df = pd.DataFrame(tabc, columns=['Tâches', 'Durée', 'Contraintes'])
    print(df)
    return df

def liste_tache(table):   # entrée : liste 1D, retourne  les taches dans stockées dans une liste de str
    tache = []

    for i  in range(1,len(table)+1):
        tache.append(str(i))

    tache.insert(0, 'a')
    tache.append('o')


    return tache

def matrice_valeurs(tabc,table):   # construit la matrice des valeurs , entrée : dataFrame du tableau de contraintes et liste 1D (respectivement), retourne la matrice des valeurs en 2D

    dure = tabc['Durée'].to_list()
    cont = tabc['Contraintes'].to_list()

    dure[0] = "0"

    # On intialise la matrice avec des "-"
    matv = [['-']*(len(table)+2) for i in range(len(table)+2)]


    tachee = liste_tache(table)
    for i in range(len(tachee)):
        for j in range(len(cont)):
            var = cont[j].split(" ")   # Il peut avoir plusierus pred
            for k in var:      # je vérifie pour chaque tache si
                if str(tachee[i]) == str(k):
                    r = j
                    tac = tachee[r]
                    if tac =="a":
                        tac = 0
                    if tac == "o":
                        tac = len(tachee) - 1
                    if isinstance(tac, str):
                        tac = int(tac)
                    if tachee[i] != "a" and tachee[i] != "o":
                        n = int(tachee[i])
                    else:
                        n = 0 if tachee[i] == "a" else len(tachee) - 1
                    matv[n][tac] = dure[i]
    return matv

def afficher_matrice_valeurs(matv,table):  # entrée : matrice des valeurs 2D str et liste 1D str , affiche la matrice des valeurs , retourne une DataFrame
    tache = liste_tache(table)
    matvpd = pd.DataFrame(matv, columns=tache, index=tache)
    print(matvpd)
    return matvpd

def detection_circuit(matv):  # entrée : DataFrame (matrice des valeurs), Detecte si il y a un circuit ,retourne booléen

    bol = True
    liste = []

    while(bol == True):
        # Parcours de la DataFrame colonne par colonne
        for col_name in matv.columns:
            if all(value == '-' for value in matv[col_name]):
                liste.append(col_name)

        if len(liste)== 0:
            bol = False
        else:
            # Si toutes les valeurs de la colonne sont égales à '-', on supprime la colonne et la ligne correspondant à l'index de la colonne
            for i in liste:
                matv = matv.drop(columns=i, index=i)
            print(matv)
            print("\n")
            liste = []



    # Vérification si toutes les colonnes ont été supprimées
    if len(matv.columns) == 0:
        print("Toutes les colonnes ont été supprimées, il n' y a pas de circuit ! \n ")
        return False
    print("Il reste des colonnes dans la DataFrame, il y a un circuit ! \n")
    return True

def calculer_rangs(matrice,table):  # entrée : DataFrame (matrice des valeurs), et liste 1D str, Calcule les rangs (on connait déjà les emplacments des taches vu que c'est des numéros, alors sur ces emplacements on met les rangs), retourne une liste 1D de str
    bol = True
    liste = []
    tache = liste_tache(table)
    rangs = ['-']*len(tache)
    r = 0

    while (bol == True):

        # Parcours de la DataFrame colonne par colonne

        for col_name in matrice.columns:
            if all(value == '-' for value in matrice[col_name]):
                liste.append(col_name)

        if len(liste) == 0:
            bol = False
        else:
            # Si toutes les valeurs de la colonne sont égales à '-', on supprime la colonne et la ligne correspondant à l'index de la colonne
            for i in liste:
                matrice = matrice.drop(columns=i, index=i)
                if(i == 'a'): i = 0
                if(i == 'o'): i = len(tache)-1
                rangs[int(i)] = str(r)

            r = r+1
            liste = []   # vider la liste

    return rangs

def liste_rang_dictionnaire(rang,table):  # rang est une liste   # table est une liste  retourne un dictionnaire des rangs avec comme keys les taches et rangs comme values
    tache = liste_tache(table)
    r  = {}
    for i in range(len(tache)):
        r[tache[i]] = rang[i]

    return r

def afficher_rangs(rangs,table):     #rangs est une liste str, et table aussi, on affiche les rangs avec Panda, retourne une liste des index
    tache = liste_tache(table)
    rangv = pd.DataFrame(rangs,index = tache,columns=["Rang"])
    rangv = rangv.sort_values(by=["Rang"])
    print(rangv)
    r = list(rangv.index)
    for i in range(len(r)):
        r[i] = r[i].strip()
    return r

def get_pred(matrice): # On utilise la DataFrame (Matrice Valeur), on retourne un dictionnaire contenant comme keys les taches et leurs predecceurs en liste de str  en values
    pred_dict = {}
    for col in matrice.columns:
        pred_list = []
        for index in matrice.index:
            value = matrice.loc[index, col]
            if value != '-':
                pred_list.append(index)
        pred_dict[col] = pred_list
    return pred_dict


def get_succ(matrice):  # On utilise la DataFrame (Matrice Valeur), on retourne un dictionnaire contenant comme keys les taches et leurs  successeurs en liste de str en values
    succ_dict = {}
    for index in matrice.index:
        succ_list = []
        for col in matrice.columns:
            if matrice.loc[index, col] != '-':
                succ_list.append(col)
        succ_dict[str(index)] = succ_list
    return succ_dict

def get_duree(matrice): # On utilise la DataFrame (Matrice Valeur), on retourne un dictionnaire contenant comme keys les taches et leurs duree  en values
    duree_dict = {}
    for index in matrice.index:
        duree_list = []
        for col in matrice.columns:
            value = matrice.loc[index, col]
            if value != '-':
                duree_list.append(value)
        if duree_list:
            duree_dict[index] = duree_list[0]
    duree_dict['o'] = 0
    return duree_dict

def calendrier_tot(pred, duree, rang):# entrée : Prends les 3 dictionnaires (predecesseurs,duree,rang) et retourne la date au plus tôt des taches sous un dictionnaire où les taches sont les keys et les dates sont les values
    date_plus_tot = {}

    for i in rang:
        t_pred = pred[i]
        if len(t_pred) == 0:
            date_plus_tot[i] = 0
        else:
            tache = t_pred[0]
            dureemax = int(duree[tache]) + int(date_plus_tot[tache]) # duree du pred
            for j in range(len(t_pred)-1):
                suivant = int(date_plus_tot[t_pred[j+1]]) + int(duree[t_pred[j+1]])
                if dureemax <= suivant:
                    dureemax = suivant
            date_plus_tot[i] = dureemax

    return date_plus_tot

def calendrier_tard(succ,duree,rang,date_plus_tot):# Entrée : Prends les 4 dictionnaires (successeurs,duree,rang,date_plus_tôt) et retourne un dictionnaire des dates au plus tard avec comme keys les taches et les dates comme values
    rang.reverse()
    date_plus_tard = {}

    for i in rang:
        t_succ = succ[i]
        if len(t_succ) == 0:
            date_plus_tard['o'] = date_plus_tot['o']
        else:
            tache = t_succ[0]
            for j in range(len(t_succ) - 1):
                suivant = int(date_plus_tard[t_succ[j + 1]])
                if int(date_plus_tard[tache]) > suivant:
                    tache = t_succ[j + 1]

            dureemax =  date_plus_tard[tache] - int(duree[i])
            date_plus_tard[i] = dureemax

    return date_plus_tard

def marge(tot,tard):  # entrée : Dictionnaires dates plus tôt et tard, retourne la marge sous la forme d'un dictionnaire où les taches sont les keys et les values les marges
    marge = {}
    for k in tot.keys():
        marge[k] = tard[k] - tot[k]
    return marge


def chemin_crit(marge, succ,duree):  #  Entrée : dictionnaires  marge, successeurs, duree .  Retourne une liste de str où les str sont des chemins critiques

    dic_chemin  = []  # liste contenant la liste des chemins
    tache_nulle = []  # on filtre d'abord les taches pour avoir seulement ceux qui ont 0 commme marge
    for k in marge.keys():
        if marge[k] == 0:
            tache_nulle.append(k)


    dic_chemin.append('a')
    bol = True
    while (bol ==True):
        for chemin in dic_chemin:   # pour chaque chemin dans le dic
            c = chemin    # un chemin
            if len(c) == 1:

                if(c[-1] !='o'):          # si la dernière tache n'est pas o
                    temp = succ[c[-1]]  # donne la liste de successeur de la tache
                    if(len(temp)== 0):     # vérifie si la tache n'a pas de succèsseurs
                        bol = False
                    else :

                        for t_nulle_succ in temp:   # boucle for pour vérifier qu'on agit sur les successeurs de marge de 0

                            if t_nulle_succ in tache_nulle :       # si le successeur est dans les taches qui ont une marge null alors
                                dic_chemin.append(chemin  + ' -> ' + t_nulle_succ) # on crée un nouveau chemin

                else :
                    bol = False


            else :
                if (c[-1] != 'o'):  # si la dernière tache n'est pas o
                    temp = succ[c.split("->")[-1].strip()]  # donne la liste de successeur de la tache
                    if (len(temp) == 0):  # vérifie si la tache n'a pas de succèsseurs
                        bol = False
                    else:

                        for t_nulle_succ in temp:  # boucle for pour vérifier qu'on agit sur les successeurs de marge de 0

                            if t_nulle_succ in tache_nulle:  # si le successeur est dans les taches qui ont une marge null alors
                                dic_chemin.append(chemin + ' -> ' + t_nulle_succ)  # on crée un nouveau chemin

                else:
                    bol = False


    # On garde les chemins qui ont la même longueur
    max = 1
    for chemin in dic_chemin:
        liste= chemin.split(' -> ')
        if(max<len(liste)) :
            max = len(liste)

    # max contient la longueur max de référence
    nouveau_dic_chemin = []
    for chemin in dic_chemin:
        liste = chemin.split(' -> ')
        if len(liste) == max:
            nouveau_dic_chemin.append(chemin)
    dic_chemin = nouveau_dic_chemin


    # Maintenant qu'on a le nombre de tache maxi , calculons les durations :
    max_duree = 0
    for chemin in dic_chemin:
        liste = chemin.split(' -> ')
        somme = 0
        for tache in liste :
            somme = somme + int(duree[tache])
        if somme>max_duree:
                max_duree = somme


    #supprimons les duree inf à la durée max :

    nouveau_dic_chemin = []
    for chemin in dic_chemin:
        liste = chemin.split(' -> ')
        somme = 0
        for tache in liste:
            somme = somme + int(duree[tache])
        if somme == max_duree:
                nouveau_dic_chemin.append(chemin)
    dic_chemin = nouveau_dic_chemin


    return dic_chemin


def affichage_calendrier_tot(rang,duree,pred,tot):  # Affiche le calendrier tôt avec une Dataframe
    df_rang = pd.DataFrame(rang.items(), columns=["Tache", "Rang"])
    df_duree = pd.DataFrame(duree.items(), columns=["Tache", "Durée"])
    df_pred = pd.DataFrame(pred.items(), columns=["Tache", "Prédécesseurs"])
    df_tot = pd.DataFrame(tot.items(), columns=["Tache", "Calendrier Tôt"])

    df = pd.merge(df_rang, df_duree, on="Tache", how="outer")
    df = pd.merge(df, df_pred, on="Tache", how="outer")
    df = pd.merge(df, df_tot, on="Tache", how="outer")

    df = df.sort_values("Rang")

    print(df)


def affichage_calendrier_tard(rang,duree,succ,tard):   # Affiche le calendrier tard avec une Dataframe
    df_rang = pd.DataFrame(rang.items(), columns=["Tache", "Rang"])
    df_duree = pd.DataFrame(duree.items(), columns=["Tache", "Durée"])
    df_succ = pd.DataFrame(succ.items(), columns=["Tache", "Successeurs"])
    df_tard = pd.DataFrame(tard.items(), columns=["Tache", "Calendrier Tard"])

    df = pd.merge(df_rang, df_duree, on="Tache", how="outer")
    df = pd.merge(df, df_succ, on="Tache", how="outer")
    df = pd.merge(df, df_tard, on="Tache", how="outer")

    df = df.sort_values("Rang")

    print(df)


def main(): # Fonction main
    arret = False

    while not arret:
        fichier = input("Inserez fichier : ")
        table = lire_fichier(fichier)
        print("\n Tableau des contraintes  : \n ")
        tab_c = constr_tabc(table)
        a_tabc = affichage_tabc(tab_c)
        matv = matrice_valeurs(a_tabc, table)
        print("\n Matrice des valeurs : \n")
        matrice = afficher_matrice_valeurs(matv, table)
        print("\n")
        print("\n Déroulement de l'algo de détection  : \n ")
        if detection_circuit(matrice) or valeur_neg(table):

            while True:
                chiffre = input("Voulez-vous travailler sur un autre graphe (1 pour oui, 0 pour non): ")
                if chiffre == '1':
                    break
                elif chiffre == '0':
                    print("Arret du projet graphe")
                    arret = True
                    break
                else:
                    print("Veuillez entrer une valeur valide (1 pour oui, 0 pour non).")
        else:
            print(" Voici les rangs  : \n")
            rang = afficher_rangs(calculer_rangs(matrice, table), table)
            print("\n Voici le calendrier tôt :  \n ")
            r = liste_rang_dictionnaire(calculer_rangs(matrice, table), table)
            duree  = get_duree(matrice)
            pred = get_pred(matrice)
            succ = get_succ(matrice)
            tot = calendrier_tot(pred, duree, rang)
            affichage_calendrier_tot(r, duree, pred, tot)
            print("\n Voici le calendrier tard : \n")
            tard = calendrier_tard(succ, duree, rang, tot)
            affichage_calendrier_tard(r, duree, succ, tard)
            print(" \n Marge : \n ")
            marg = marge(tot, tard)
            print(marg)
            print(" \n Voici le(s) chemin(s) critique(s) : \n")
            ch  = chemin_crit(marg, succ, duree)
            for i in range(len(ch)):
                print("Chemin numéro : ", i+1)
                print("\n" ,ch[i],"\n")

            while True:
                chiffre = input("Voulez-vous travailler sur un autre graphe (1 pour oui, 0 pour non): ")
                if chiffre == '1':
                    break
                elif chiffre == '0':
                    print("Arret du projet graphe")
                    arret = True
                    break
                else:
                    print("Veuillez entrer une valeur valide (1 pour oui, 0 pour non).")




main()