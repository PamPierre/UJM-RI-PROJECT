#!/usr/bin/env python
# coding: utf-8

# In[108]:


# Cell for imports
import re
import os
import gzip
import time
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from stop_words import get_stop_words
from zipfile import ZipFile
import math


#### Cell of all my function

def list_file_data(nom_directory):
    myListFile = []
    for f in os.listdir(nom_directory):
        if os.path.isdir(f): # si f est un dossier
            os.chdir(f) # On va lister son contenu
            parse()
            os.chdir('../') # On revient au répertoire précédent
        else:
            myListFile.append(f)
        # Traitement sur le fichier f
    return myListFile

def preprocesFile(fileName):
    if '.gz' in fileName:
        file_content = gzip.open(fileName, 'rb')
    elif ".zip" in fileName:
        name = fileName.split('/')[1].replace('.zip','')
        with ZipFile(fileName) as myzip:
            with myzip.open(name) as myfile:
                file_content=myfile.read()
    return file_content


def preprocesDataFile(fileName):
    full_text = preprocesFile(fileName)
    docListNum = re.findall('<doc><docno>(.*?)</docno>(.*?)</doc>', str(full_text).lower().strip())
    list_doc = re.findall('<doc><docno>(.*?)</docno>', str(full_text).strip())
    return docListNum, list_doc

def clean(text1,use_stopword_stemmer):
    remove_w = "_:/!?#^*~&()[]{}';$%|,.-"
    stopwords = get_stop_words('english')
    full_text = text1.lower().replace('\\n', '').strip(remove_w).replace("''",' ').replace("'",' ')
    full_text = re.sub(r'[^\w\s]', '', full_text) # Remove all punctuation
    if(use_stopword_stemmer):
        full_text = [stemmer.stem(word) 
                     for word in full_text.split() 
                     if len(word)>1 
                     and word not in stopwords 
                     and not word.isnumeric() 
                     and word.isalnum()] ### remove stops_word and applique stemming
        #full_text = [word for word in full_text.split() if len(word)>1 and word not in stw and not word.isnumeric()] ### remove word and applique stemming
    else:
        full_text = [word 
                     for word in full_text.split() 
                     if len(word)>1  
                     and not word.isnumeric()
                     and word.isalnum()] 
    return ' '.join(full_text)


def countWord(words):   
    word_count = {} # compte l'occurance d'un terme dans tous les documents
    j=0
    for word in words: # On parcours la listes de mots
        j+=1
        word  = word.lower()
        if (len(word)==1) or str(word).isnumeric() or str(word).isnumeric():
            continue
        if not word in word_count:
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1
    return word_count

def countWordIntoDocs(dico, docno, posting):
    docname = docno
    
    for word, frequence in dico.items():
        posting.setdefault(word,[]).append((docname,frequence)) ### Remplace les lignes de commande suivante:
        """
        if not word in list(posting.keys()):
            posting[word] = [(docname, frequence)]
        else:
            posting[word].append((docname, frequence))
        """
    return posting

def doc_len(list_terms):
    dl = [(doc_n, len(len_doc)) for doc_n,len_doc in list_terms.items()]
    return dl

def vocabulary_size(posting_list):
    return len(posting_list.keys())


def term_len(posting_list):
    # Return 
    return [(term, len(term)) for term in posting_list.keys()]

def collection_term_freq(posting_list):
    c_size={}
    dl = {}
    print(posting_list)
    for term,values in posting_list.items(): # get the term
        somme=0
        for v in values:
            somme+=v[1]
        dl[term]=[(somme,len(values))]
    return dl
        
## Pour avoir une courbe avec le plot
def plot_datas(data, title, label_x, label_y):
    x = list()
    y = list()
    for key, values in data.items():
        x.append(key)
        y.append(values[0])
    plt.plot(x,y, color='blue',marker='o',linestyle='solid')
    #Titre
    plt.title(title)
    # label
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()
    
## Fonction de traintement du texte  
def text_mining(fileName,use_stopword_stemmer=bool()):
    start = time.time()
    docListNum, list_doc = preprocesDataFile(fileName)
    posting_list = {}
    file_number = fileName.split('/')[1].split('-',1)
    dl = list()
    for i in range(len(list_doc)):
        text_clean = clean(docListNum[i][1],use_stopword_stemmer)
        list_terms[list_doc[i]] = text_clean.split() # Here we create a dictionary of Here we create a dictionary of 
                                                                              # each docments with its terms
        lt = text_clean.split()
        current_dico = countWord(lt)
        posting_list = countWordIntoDocs(current_dico, list_doc[i], posting_list)
    end = time.time()
    elapsed = end - start
    tf = term_len(posting_list)
    file_indexing_infos=(round(elapsed,3),tf)
    return posting_list, list_terms

def smart_ltn(posting_list,n, c_tf):
    #=(1+LOG(tf))*LOG(n/c_tl)
    ltn = {}
    for key, value in posting_list.items():
        for v in value:
            tf = 1+math.log(v[1])
        for v in c_tf[key]:
            c_tl = v[1]
        if c_tl==0:
            ltn[key] = 0
        else:
            ltn[key] = tf*math.log(n/c_tl)
    ltn_sum = sum(ltn.values())
    return ltn_sum

def get_statistics(posting_list,list_terms):
    stat = {}
    # document length
    stat['df'] = doc_len(list_terms)
    # Number of a doc
    stat['n_doc'] = len(stat['df'])
    # term length
    stat['tl'] = term_len(posting_list)
    #vocabulary size
    stat['voc_size'] = vocabulary_size(posting_list)
    #collection frequency of terms
    stat['colec_freq'] = collection_term_freq(posting_list)
    return stat

def scoring_doc(query_clean, pl, lt):
    rsv = {}
    stat = get_statistics(pl,lt)
    for q in query_clean.split():
        if q in pl.keys():
            #tf = [f[1] for f in pl[q]]
            for v in pl[q]:
                tf = (v[1]/len(lt[v[0]]))
                idf = math.log(stat['n_doc'] / len(pl[q]))
                #val = (1+math.log(value[1]))/math.log(stat['n_doc']/tf)
                rsv.setdefault(v[0],[]).append((tf*idf))
    rsv = [(doc,sum(v)) for doc,v in rsv.items()]
    return rsv

### Cell to initialise variable.
directory = "Practice_02_data/"
list_data = list_file_data(directory)
list_data = sorted(list_data)
list_char = "_:/!?#^*~&()[]{}';$%|,.-"
posting_list = {}
posting_list_global = {}
file_indexing_infos = {}
dl = {}
tf = {}
stopwords = get_stop_words('english')
list_terms = {}
stemmer = PorterStemmer()


