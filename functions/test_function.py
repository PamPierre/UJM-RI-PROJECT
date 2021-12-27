from file_process import *
from text_process import *
list_file = list_file_data("../Practice_05_data/XML-Coll-withSem/")

dataset = "../Practice_05_data/XML-Coll-withSem/"
list_termes = {}
for file_name in list_file:
    print(file_name)
    list_termes= splitDocs(dataset+file_name,list_termes)
print(len(list_termes))