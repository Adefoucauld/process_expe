# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 12:29:40 2021

@author: Utilisateur
"""
'''Librairies utiles pour le scan direct '''
from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import tkinter
from tkinter import *

'''librairies utiles pour le cmr'''

from generation_cmr import *

# fenetre = Tk() 

'''Creation dictionnaire tournée'''

planning_tournee = dict()
planning_tournee = {
    
    18 : {
        'matin' : [219,231,308],
        'apm' : [223,207] 
        },
    19 : {
        'matin' : [20,44],
        'apm' : [30,35] 
        },
    20 : {
        'matin' : [18,26],
        'apm' : [9,21,239,236] 
        },
    21 : {
        'matin' : [24,202],
        'apm' : [214,201] 
        },
    22 : {
        'matin' : [14,15,29],
        'apm' : [43,5] 
        },
    23 : {
        'matin' : [204,23],
        'apm' : [45,32,220] 
        },
    24 : {
        'matin' : [233,235,240],
        'apm' : [] 
        },
    25 : {
        'matin' : [203],
        'apm' : [243,28] 
        },
    26 : {
        'matin' : [7,1],
        'apm' : [33,226] 
        },
    27 : {
        'matin' : [19,10],
        'apm' : [228,224,210] 
        },
    28 : {
        'matin' : [34,230,232],
        'apm' : [216,41] 
        },
    29 : {
        'matin' : [],
        'apm' : [22,2,12,36,241] 
        },
    30 : {
        'matin' : [39,217,310],
        'apm' : [8,4] 
        },
    31 : {
        'matin' : [206,16,208,227,42],
        'apm' : [] 
        },
    32 : {
        'matin' : [238,234,237],
        'apm' : [212,213,27] 
        },
    33 : {
        'matin' : [311,11,38],
        'apm' : [211,25] 
        },
        
        }

''' Recupération des palettes plannifiées '''

df = pd.read_excel(r'C:/Users/Utilisateur/Documents/FNAC_VDB/Projet_expe/test_tot_shop_pal.xlsx')
#on traite l'absence de données Nan en remplaçant par 0
df = df.fillna(0) 

#on crée une liste des shop 
shop_pal = list(df.columns)
shop_pal = [int(x//10) for x in shop_pal]

#on utilise format des dictionnaire pour nos objet
pal = dict()
err_pal = dict()

#regroupement de pal par shop
for col in df.columns:  #on génère les listes de pal planifiés pour chaque shop
        l = list(df[col])
        l = [int(x//10) for x in l if x != 0]
        num = int(col)
        pal[num//10] = l
        err_pal[num//10] = {'pal_ds_autre_shop':[],
                            'err_scan':[]
                            }

nb_shop = len(shop_pal)
    
''' fonctions reconnaissance pour rendre code plus lisible'''
def is_shop(tmp):
    if tmp//1000 == 0:
        return(True)
    return(False)

def is_barcode(tmp):
    if tmp//100000 !=0 :
        return (True)
    return(False)

def is_fin_scan(tmp):
    if tmp == 888888888888:
        return(True)
    return(False)

def is_correction(tmp):
    if tmp == 3:
        return(True)
    return(False)

def is_extra(tmp):
    if tmp ==999999999999:
        return(True)
    return(False)

def is_matin(tmp):
    if tmp == 10000:
        return(True)
    return(False)

def is_apm(tmp):
    if tmp == 11845678901001:
        return(True)
    return(False)      

def is_dacem(tmp):
    if tmp == 0:
        return(True)
    return(False)

''' fonctions associées à la lecture d'un code barre particulier'''

#lecture d'un code barre shop
def scan_shop(tmp,w):
    #on affiche bouton 'ok'
    Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
    
    #on remet tous les shops de la même couleur
    for num in shop_plan:
        idx = shop_plan.index(num)
        Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column=idx)
    #on repère le magasin que l'on a scanné
    index = shop_plan.index(tmp)
    #on ajoute à la liste des indices des shops scannés
    list_idx.append(index)
    Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4, bg = "yellow").grid(row=0,column = index)
    
#lecture d'une tournée    
def scan_tournee(tmp,tournee,liv):
    #on définit des variables globale car on a besoin de les utiliser
    global shop_plan,R
    R = dict()
    
    #on regarde si on a bien scanné un n° de tournée
    if tmp not in planning_tournee.keys():
        #si ce n'est pas le cas on affiche un message d'erreur
        Button(w,text = " Veuillez scanner un n° de tournée " ,bg = "red", width = 30).grid(row= 2, column = 7)
        entree.delete(0,END)
    else:
        #si c'est le cas, on regarde la tournée qui est associée
        Button(w,text = " Ok !", width = 30).grid(row= 2, column = 7)
        shop_plan = planning_tournee[tmp][liv[-1]]
        #on génère notre historique de scan de type dict
        R = {x:[] for x in shop_plan}
        
        #on ajoute les clés DACEM et TOURNEE, utiles ensuite
        R['tournee'] = [tmp]
        R['dacem']=dict()
        
        #on affiche les palettes plannifiées pour chaque magasin de la tournée
        for num in shop_plan:
            R['dacem'][num] = 0
            Button(w, text = "DACEM "+ str(R['dacem'][num]),borderwidth = 4).grid(row=1,column= shop_plan.index(num))
            Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column= shop_plan.index(num))
            nb_pal = len(pal[num])
            for i in range(nb_pal):
                Button(w,text = str(pal[num][i]),borderwidth = 1, bg = "white",width = 30).grid(row = i+2, column = shop_plan.index(num))
        #on enregistre le fait que l'on a déjà scanné un n° de tournée
        tournee.append(True)
        entree.delete(0,END)

def scan_extra(tmp,extra):
    #on crée les variables globales nécessaires au code dans le cas d'un EXTRA
    global shop_plan,R
    shop_plan = []
    R = dict()    
    #on ajoute une clé EXTRA à notre historique de scan
    R['tournee'] = 'Extra'
    R['dacem'] = dict()
    Button(w,text = " EXTRA " ,bg = "orange", width = 30).grid(row= 0, column = 7)
    #on garde en mémoire que l'on a scanné un extra
    extra.append(True)
    #on garde en mémoire que l'on a plus besoin de scanner une tournée
    tournee.append(True)
    entree.delete(0,END)
    
def fin_shop_extra(tmp,extra):
    #on indique que l'on est sorti du mode 'EXTRA'
    extra.append(False)
    #on indique sur interface les étapes à suivre
    Button(w, text ='Select shop à charger', width = 30).grid(row = 2,column = 7)
    entree.delete(0,END)
    
def fin_scan(tmp):
    #on indique que l'on a fini le scan
    Button(w, text ='Fin du scan', width = 30).grid(row = 2,column = 7)
    exit_button = Button(w, text="Exit", command=w.destroy, width = 20, bg = 'pink') 
    exit_button.grid(row=4, column = 7)
    
''' declarations variables globales'''


correction= [False] #indicateur de correction
good_scan=[] #historique global des palettes bien scannées
list_idx =[] #historique des shops scannés
tournee = [False]  #indicateur de tournée
extra = [False]  #indicateur d'extra
liv=[]           # indicateur de horaire de tournée

'''Fonction de sortie accessoire'''

def quit_pal(event):
    w.destroy()

''' fonction d'actualisation de la fenêtre graphique'''

def rec_name(event):
    #on supprime la clé de contrôle de chaque code barre
    tmp = int(value.get())//10 
    
    #on ne veut pas pouvoir scanner extra dans une tournee (extra prio sur la tournée)
    if is_extra(tmp) : 
        lbl_scan = Label(w, text = "Scanner Code barre ")
        lbl_scan.grid(row=1,column = 6, padx = 5, pady = 5)
        #on regarde si c'est pour ouvrir la création d'une tournee extra ou pour la fermer
        if not extra[-1] and len(tournee)<2:
            #on va venir ajouter des shops dans la tournee
            scan_extra(tmp, extra)
        else:
            #on arrete d'ajouter des shops et on commence à scanner
            fin_shop_extra(tmp, extra)
    
    #on scan un code-barre matin
    elif is_matin(tmp):
        lbl_scan = Label(w, text = "Scanner Code barre ")
        lbl_scan.grid(row=1,column = 6, padx = 5, pady = 5)
        liv.append('matin')
        Button(w,text ='MATIN : Scanner n° de tournée',width = 30).grid(row=2, column = 7)
        entree.delete(0,END)
        
    #on scan un code_barre apm pour la tournée    
    elif is_apm(tmp):
        lbl_scan = Label(w, text = "Scanner Code barre ")
        lbl_scan.grid(row=1,column = 6, padx = 5, pady = 5)
        liv.append('apm')
        Button(w,text ='APM : Scanner n° de tournée',width = 30).grid(row=2, column = 7)
        entree.delete(0,END)
     
    #on commence process de correction    
    elif is_correction(tmp) :
        #on vérifie que c'est pour commencer une correction
        if not correction[-1]:
            correction.append(True)
            # Button(w,text ='Scanner shop à corrriger',width = 30).grid(row=2, column = 7)
            Button(w,text ='Scanner pal à corrriger',width = 30).grid(row=2, column = 7)
            entree.delete(0,END)
        else:
            correction.append(False)
            entree.delete(0,END)
     
    #on scan un n° de tournée        
    elif not tournee[-1]and not extra[-1]: #on scan une tournee
        scan_tournee(tmp,tournee,liv)
    
    #on scan un dacem
    elif is_dacem(tmp):
        #on s'assure qu'un n° de magasin a bien été scanné avant
        if len(list_idx)<1:
            #si non on affiche un message d'erreur
            Button(w,text ='Scanner un n° de shop',width = 30,bg='red').grid(row=2, column = 7)
            entree.delete(0,END)
        else:
            #si oui on additionne +1 au compteur de DACEM
            num = shop_plan[list_idx[-1]]
            R['dacem'][num] +=1
            Button(w, text = "DACEM : "+ str(R['dacem'][num]),borderwidth = 4).grid(row=1,column= shop_plan.index(num))
            entree.delete(0,END)
        
    else: 
        #on scan forcment un n° de shop ou de palette
        
        #creation de la tournee extra, on va ajouter les shops scannés
        if extra[-1] and is_shop(tmp):  
            Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
            shop_plan.append(tmp)
            R[tmp]=[]
            idx = shop_pal.index(tmp)
            R['dacem'][tmp] = 0
            Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4).grid(row=0,column= shop_plan.index(tmp))
            Button(w, text = "DACEM "+ str(R['dacem'][tmp]),borderwidth = 4).grid(row=1,column= shop_plan.index(tmp))
            nb_pal = len(pal[tmp])
            for i in range(nb_pal):
                Button(w,text = str(pal[tmp][i]),borderwidth = 1, bg = "white",width = 30).grid(row = i+2, column = shop_plan.index(tmp))
           
       #on est dans un process de correction et on scan un shop
            '''version où on ne scanne pas le shop pour la correction'''
        # elif correction[-1] and is_shop(tmp):
        #     Button(w, text ='Scanner palette à retirer', width = 30).grid(row = 2,column = 7)
        #     for num in shop_plan:
        #         idx = shop_plan.index(num)
        #       #On remet tous les shops en gris
        #         Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column=idx)
        #     list_idx.append(shop_plan.index(tmp))
        #   #on affiche en jaune le shop sélectionné pour la correction
        #     Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4, bg = "yellow").grid(row=0,column = shop_plan.index(tmp))
        
        #on scan un shop dans un process de scan normal
        elif is_shop(tmp) and tmp in shop_plan and not extra[-1]:
            scan_shop(tmp, w)
        
        #on scan un barcode
        elif is_barcode(tmp) and not is_fin_scan(tmp): #c'est  un barcode
            #on regarde si on a bien scanné un n° de shop avant
            if len(list_idx)==0  : #scanné avant shop 
                btn = Button(w,text = " ERREUR : Scanner un n° de shop ", bg = "red", width = 30)
                btn.grid(row = 2, column = 7)
            
            #on scan un barcode "correction"
            elif correction[-1]:
                '''version où on doit scanner un shop avant de scanner une palette'''
                # Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                # num_idx = list_idx[-1]
                # if tmp in R[shop_plan[num_idx]]:
                #     R[shop_plan[num_idx]].remove(tmp)
                # else:
                #     Button(w,text = "Palette pas dans ce shop",bg = "red", width = 30).grid(row = 2,column = 7)
                #     entree.delete(0,END)
                # idx2 = pal[shop_plan[num_idx]].index(tmp)
                # Button(w,text = str(pal[shop_plan[num_idx]][idx2]),bg = "white", width = 30).grid(row = idx2+2,column = num_idx)
                # entree.delete(0,END)
                
                '''Version où on peut scanner directement la palette'''
                verif = True
                Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                #on doit retrouver la palette et le shop correspondant
                for shop in shop_plan:
                    if tmp in R[shop] :
                        num_idx = shop_plan.index(shop)
                        R[shop].remove(tmp)
                        idx2 = pal[shop].index(tmp)
                        Button(w,text = str(pal[shop][idx2]),bg = "white", width = 30).grid(row = idx2+2,column = num_idx)
                        verif = False
                        entree.delete(0,END)
                #on vérifie que la palette qu'on veut corriger a bien été scannée
                if verif:
                    Button(w,text = "Palette pas scannée ",bg = "red", width = 30).grid(row = 2,column = 7)
                    entree.delete(0,END)
            
            #on scan un barcode normal
            else:
                num = list_idx[-1] #on récup l'idx du num du shop en cours
                idx = shop_pal.index(shop_plan[num])         
                #si palette est planifiée pour ce magasin
                if tmp in pal[shop_plan[num]]:
                    if tmp not in good_scan:
                        R[shop_pal[idx]].append(tmp)
                    good_scan.append(tmp)
                    
                    idx2 = pal[shop_plan[num]].index(tmp)
                    Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                    Button(w,text = str(pal[shop_plan[num]][idx2]),bg = "green", width = 30).grid(row = idx2+2,column = num)
                
                #palette pas assignée au shop en cours
                else:
                    # l=[tmp,num]
                    
                    #une palette bien scannée ne va pas être remodifiée
                   
                    is_ref = False
                        
                    #on recherche le shop auquel la palette correspond
                    for num_shop in shop_pal:
                        if tmp in pal[num_shop]:
                            is_ref = True
                            Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                            #on garde en mémoire les erreurs de scan faites 
                            err_pal[shop_plan[num]]['err_scan'].append([tmp," Shop n° ", num_shop])
                            err_pal[num_shop]['pal_ds_autre_shop'].append([tmp,"shop n°",shop_plan[num]])
                            
                            Button(w,text = str(tmp)+" Shop n° "+ str(num_shop),bg = "red", width = 30).grid(row= len(pal[shop_plan[num]])+len(err_pal[shop_plan[num]]['err_scan'])+1, column = num)
                           
                            #on regarde si la palette est planifiée pour un autre shop de la livraison
                            if tmp not in good_scan:
                                idx_pal_scan = pal[num_shop].index(tmp)
                                if num_shop in shop_plan:
                                    Button(w,text = str(tmp)+ " Scannée dans shop n° " + str(shop_plan[num]), bg = "blue", width = 30).grid(row =idx_pal_scan +2, column = shop_plan.index(num_shop))
                                else:
                                    pal[num_shop][idx_pal_scan] = [tmp,shop_plan[num]]
                    
                    #si le code barre n'est pas dans la base de données, on indique sur le terminal
                    if not is_ref:   
                        Button(w,text = str(tmp)+" Code barre inconnu" ,bg = "red", width = 30).grid(row= 2, column = 7)
       
        #on scan le barcode fin de scan
        elif is_fin_scan(tmp):
           fin_scan(tmp)
           
        #on scan un barcode non répertorié donc on affiche un message d'erreur
        else:
             Button(w,text = str(tmp)+" Code barre inconnu" ,bg = "red", width = 30).grid(row= 2, column = 7)
        entree.delete(0,END)




''' Lancement fenêtre Tkinter'''

#on ouvre la fenetre graphique
w = Tk()
w.title("Scan expédition")

lbl_scan = Label(w, text = "Matin/Apm/Extra ? ")
lbl_scan.grid(row=1,column = 6, padx = 5, pady = 5)

#on récupère l'entrée donnée par le gun
value = StringVar() 
value.set("")
entree = Entry(w, textvariable= value)
entree.grid(row = 1, column = 7, padx = 5, pady = 5)
entree.bind("<Return>", rec_name)

w.bind("<Double-Escape>", quit_pal)   
w.mainloop() 


'''Traitement scan et génération CMR'''

#une fois le scan terminé, on génère le CMR

gene_cmr(R,pal,shop_pal) 



