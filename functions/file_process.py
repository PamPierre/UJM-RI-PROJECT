import re
import os
import gzip
import time
import matplotlib.pyplot as plt
from zipfile import ZipFile
import math
from bs4 import BeautifulSoup


def list_file_data(nom_directory):
    myListFile = []
    for f in os.listdir(nom_directory):
        if os.path.isdir(f): # si f est un dossier
            os.chdir(f) # On va lister son contenu
            os.chdir('../') # On revient au répertoire précédent
        else:
            myListFile.append(f)
        # Traitement sur le fichier f
    return myListFile

def preprocesFile(fileName):
    print(fileName)
    if '.gz' in fileName:
        file_content = gzip.open(fileName, 'rb')
        file_content = file_content.read()
    elif ".zip" in fileName:
        name = fileName.split('/')[1].replace('.zip','')
        with ZipFile(fileName) as myzip:
            with myzip.open(name) as myfile:
                file_content=myfile.read()
    else :
        with open(fileName) as file:
            file_content = file.read()
    return file_content

def splitDocs(fileDoc, list_terme):
    content = []
      # Read the XML file
    with open(fileDoc, "r",encoding='utf-8') as file:
      # Read each line in the file, readlines() returns a list of lines
      content = file.readlines()
      # Combine the lines in the list into a string
      content = " ".join(content)
      soup = BeautifulSoup(content, "xml")
      id = str(soup.find_all('id')[0]).strip('</id>')
      sec = soup.find_all('sec')
      #text =  soup.get_text()
      list_terme[id]=sec  # Pour chaque article on recuper les sections
      print(sec)
    return list_terme

def splitDocs1(fileDoc):
  content = []
  # Read the XML file
  with open(fileDoc, "r",encoding='utf-8') as file:
      # Read each line in the file, readlines() returns a list of lines
      content = file.readlines()
      # Combine the lines in the list into a string
      content = " ".join(content)
      soup = BeautifulSoup(content, "xml")
      sec=soup.find_all('sec')
  return sec






# print(corpus['id1'][0]['sec1'][0]['span'])