# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 12:29:40 2021

@author: Utilisateur
"""
'''Librairies utiles pour le scan direct '''
from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
from datetime import datetime # pour importer la date 
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
df = df.fillna(0) 


shop_pal = list(df.columns)
shop_pal = [int(x//10) for x in shop_pal]
pal = dict()
err_pal = dict()
#regroupement de pal par shop

for col in df.columns:  #on génère les listes de pal planifiés pour chaque shop
        l = list(df[col])
        l = [int(x//10) for x in l if x != 0]
        num = int(col)
        pal[num//10] = l
        err_pal[num//10] = []

nb_shop = len(shop_pal)
    
''' fonctions reconnaissance'''
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

def scan_shop(tmp,w,err_first):
    Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
    if err_first[-1] : 
        err_first[-1]= False
    #on remet tous les shops de la même couleur
    for num in shop_plan:
        idx = shop_plan.index(num)
        Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column=idx)
    index = shop_plan.index(tmp)
    list_idx.append(index)
    Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4, bg = "yellow").grid(row=0,column = index)
    Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
    if err_first[-1] : 
        err_first[-1]= False
    #on remet tous les shops de la même couleur
    for num in shop_plan:
        idx = shop_plan.index(num)
        Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column=idx)
    index = shop_plan.index(tmp)
    list_idx.append(index)
    Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4, bg = "yellow").grid(row=0,column = index)

    
def scan_tournee(tmp,tournee,liv):
    global shop_plan,R
    R = dict()
    if tmp not in planning_tournee.keys():
        Button(w,text = " Veuillez scanner un n° de tournée " ,bg = "red", width = 30).grid(row= 2, column = 7)
        entree.delete(0,END)
    else:
        Button(w,text = " Ok !", width = 30).grid(row= 2, column = 7)
        # now = datetime.now().time()
        # hour = datetime(1,1,1,10,0,0,0)   #ON FIXE A 10H LE DEBUT DE LA DEUXIEME TOURNEE
        # hour = hour.time()
        # if now < hour:
        #     liv = 'matin'
        # else:
        #     liv = 'apm'
        shop_plan = planning_tournee[tmp][liv[-1]]
        R = {x:[] for x in shop_plan}
        R['tournee'] = [tmp]
        R['dacem']=dict()
        for num in shop_plan:
            R['dacem'][num] = 0
            Button(w, text = "DACEM "+ str(R['dacem'][num]),borderwidth = 4).grid(row=1,column= shop_plan.index(num))
            Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column= shop_plan.index(num))
            nb_pal = len(pal[num])
            for i in range(nb_pal):
                Button(w,text = str(pal[num][i]),borderwidth = 1, bg = "white",width = 30).grid(row = i+2, column = shop_plan.index(num))
        tournee.append(True)
        entree.delete(0,END)

def scan_extra(tmp,extra):
    global shop_plan,R
    shop_plan = []
    R = dict()    
    R['tournee'] = 'Extra'
    Button(w,text = " EXTRA " ,bg = "orange", width = 30).grid(row= 2, column = 7)
    extra.append(True)
    tournee.append(True)
    entree.delete(0,END)
    
def fin_shop_extra(tmp,extra):
    extra.append(False)
    Button(w, text ='Select shop à charger', width = 30).grid(row = 2,column = 7)
    entree.delete(0,END)
    
def fin_scan(tmp):
    Button(w, text ='Fin du scan', width = 30).grid(row = 2,column = 7)
    exit_button = Button(w, text="Exit", command=w.destroy, width = 20, bg = 'pink') 
    exit_button.grid(row=4, column = 7)
    
''' declarations variables globales'''

correction= [False]
good_scan=[]
list_idx =[]
err_first = [False]
tournee = [False] 
extra = [False]
liv=[]

'''Fonction de sortie '''

def quit_pal(event):
    w.destroy()

''' fonction d'actualisation de la fenêtre graphique'''

def rec_name(event):
    tmp = int(value.get())//10 
    
    if is_extra(tmp) : #on ne veut pas pouvoir scanner extra dans une tournee
        if not extra[-1] and len(tournee)<2:
            scan_extra(tmp, extra)
            R['dacem']=dict()
        else:
            fin_shop_extra(tmp, extra)
    
    elif is_matin(tmp):
        liv.append('matin')
        Button(w,text ='MATIN : Scanner n° de tournée',width = 30).grid(row=2, column = 7)
        entree.delete(0,END)
        
    elif is_apm(tmp):
        liv.append('apm')
        Button(w,text ='APM : Scanner n° de tournée',width = 30).grid(row=2, column = 7)
        entree.delete(0,END)
        
    elif is_correction(tmp) :
        if not correction[-1]:
            correction.append(True)
            Button(w,text ='Scanner shop à corrriger',width = 30).grid(row=2, column = 7)
            entree.delete(0,END)
        else:
            correction.append(False)
            entree.delete(0,END)
            
    elif not tournee[-1]and not extra[-1]: #on scan une tournee
        scan_tournee(tmp,tournee,liv)
        
    elif is_dacem(tmp):
        if len(list_idx)<1:
            Button(w,text ='Scanner un n° de shop',width = 30,bg='red').grid(row=2, column = 7)
            entree.delete(0,END)
        else:
            num = shop_plan[list_idx[-1]]
            R['dacem'][num] +=1
            Button(w, text = "DACEM : "+ str(R['dacem'][num]),borderwidth = 4).grid(row=1,column= shop_plan.index(num))
            entree.delete(0,END)
        
    else: 
        
        if extra[-1] and is_shop(tmp):  #creation de la tournee extra
            shop_plan.append(tmp)
            R[tmp]=[]
            idx = shop_pal.index(tmp)
            R['dacem'][tmp] = 0
            Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4).grid(row=0,column= shop_plan.index(tmp))
            Button(w, text = "DACEM "+ str(R['dacem'][tmp]),borderwidth = 4).grid(row=1,column= shop_plan.index(tmp))
            nb_pal = len(pal[tmp])
            for i in range(nb_pal):
                Button(w,text = str(pal[tmp][i]),borderwidth = 1, bg = "white",width = 30).grid(row = i+2, column = shop_plan.index(tmp))
            
        elif correction[-1] and is_shop(tmp):
            Button(w, text ='Scanner palette à retirer', width = 30).grid(row = 2,column = 7)
            for num in shop_plan:
                idx = shop_plan.index(num)
                Button(w, text = "Shop n° "+ str(num),borderwidth = 4).grid(row=0,column=idx)
            list_idx.append(shop_plan.index(tmp))
            Button(w, text = "Shop n° "+ str(tmp),borderwidth = 4, bg = "yellow").grid(row=0,column = shop_plan.index(tmp))
        
        elif is_shop(tmp) and tmp in shop_plan and not extra[-1]:
            scan_shop(tmp, w, err_first)
               
            
        elif is_barcode(tmp) and not is_fin_scan(tmp): #c'est  un barcode
            if len(list_idx)==0  : #scanné avant shop 
                err_first.append(True)
                btn = Button(w,text = " ERREUR : Scanner un n° de shop ", bg = "red", width = 30)
                btn.grid(row = 2, column = 7)
            
            elif correction[-1]:
                Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                num_idx = list_idx[-1]
                R[shop_plan[num_idx]].remove(tmp)
                idx2 = pal[shop_plan[num_idx]].index(tmp)
                Button(w,text = str(pal[shop_plan[num_idx]][idx2]),bg = "white", width = 30).grid(row = idx2+2,column = num_idx)
                entree.delete(0,END)
            
            else:
                num = list_idx[-1] #on récup l'idx du num du shop en cours
                idx = shop_pal.index(shop_plan[num])         
                #si palette planifiée
                if tmp in pal[shop_plan[num]]:
                    if tmp not in good_scan:
                        R[shop_pal[idx]].append(tmp)
                    good_scan.append(tmp)
                    
                    idx2 = pal[shop_plan[num]].index(tmp)
                    Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                    Button(w,text = str(pal[shop_plan[num]][idx2]),bg = "green", width = 30).grid(row = idx2+2,column = num)
                
                #palette pas assignée au shop en cours
                else:
                    l=[tmp,num]
                    
                    #une palette bien scannée ne va pas être remodifiée
                   
                    is_ref = False
                        
                        #on recherche le shop auquel la palette correspond
                    for num_shop in shop_pal:
                        if tmp in pal[num_shop]:
                            is_ref = True
                            Button(w, text ='Ok !', width = 30).grid(row = 2,column = 7)
                            err_pal[shop_plan[num]].append([tmp," Shop n° ", num_shop])
                            Button(w,text = str(tmp)+" Shop n° "+ str(num_shop),bg = "red", width = 30).grid(row= len(pal[shop_plan[num]])+len(err_pal[shop_plan[num]])+1, column = num)
                           
                            if tmp not in good_scan:
                                idx_pal_scan = pal[num_shop].index(tmp)
                                if num_shop in shop_plan:
                                    Button(w,text = str(tmp)+ " Scannée dans shop n° " + str(shop_plan[num]), bg = "blue", width = 30).grid(row =idx_pal_scan +2, column = shop_plan.index(num_shop))
                            
                    if not is_ref:   
                        Button(w,text = str(tmp)+" Code barre inconnu" ,bg = "red", width = 30).grid(row= 2, column = 7)
        
        elif is_fin_scan(tmp):
            fin_scan(tmp)
            
        else:
             Button(w,text = str(tmp)+" Code barre inconnu" ,bg = "red", width = 30).grid(row= 2, column = 7)
        entree.delete(0,END)




''' Lancement fenêtre Tkinter'''

w = Tk()
w.title("Pal plan")

lbl_scan = Label(w, text = "Scan code-barre tournée ")
lbl_scan.grid(row=1,column = 6, padx = 5, pady = 5)


value = StringVar() 
value.set("")
entree = Entry(w, textvariable= value)
entree.grid(row = 1, column = 7, padx = 5, pady = 5)
entree.bind("<Return>", rec_name)

w.bind("<Double-Escape>", quit_pal)   
w.mainloop() 


'''Traitement scan et génération CMR'''


gene_cmr(R,pal,shop_pal) 



