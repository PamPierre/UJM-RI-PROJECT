from file_process import *
from nltk.stem import PorterStemmer
from stop_words import get_stop_words

def preprocesDataFile(fileName):
    full_text = preprocesFile(fileName)
    docListNum = re.findall('<doc><docno>(.*?)</docno>(.*?)</doc>', str(full_text).lower().strip())
    list_doc = re.findall('<doc><docno>(.*?)</docno>', str(full_text).strip())
    return docListNum, list_doc


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
      text =  soup.get_text()
      list_terme[id]=text
    return list_terme

def clean(text1, use_stem, use_stopword):
    stopwords = get_stop_words('english')
    stemmer = PorterStemmer()
    full_text = text1.lower().replace('\\n', '').replace("'", ' ')
    full_text = re.sub(r'[^\w\s]', '', full_text)  # Remove all punctuation
    text = list()
    for word in full_text.split():
        if len(word) > 2 and word.isalpha():
            if not use_stopword:
                if use_stem:
                    text.append(stemmer.stem(word))
                else:
                    text.append(word)
            elif word not in stopwords:
                if use_stem:
                    text.append(stemmer.stem(word))
                else:
                    text.append(word)
    full_text = text
    return ' '.join(full_text)


def doc_len(list_terms):
    dl = {}
    for doc_n, len_doc in list_terms.items():
        dl[doc_n] = len(len_doc)
    # dl = [(doc_n, len(len_doc)) for doc_n,len_doc in list_terms.items()]
    return dl


def vocabulary_size(posting_list):
    return len(posting_list.keys())


def term_len(posting_list):
    # Return
    return [(term, len(term)) for term in posting_list.keys()]


def collection_term_freq(posting_list):
    c_size = {}
    dl = {}
    for term, values in posting_list.items():  # get the term
        somme = 0
        for v in values:
            somme += v[1]
        dl[term] = [(somme, len(values))]
    return dl


def countWord(words):
    word_count = {} # compte l'occurance d'un terme dans tous les documents
    j=0
    for word in words: # On parcours la listes de mots
        word  = word.lower()
        if (len(word)==1) or str(word).isnumeric() or str(word).isnumeric():
            continue
        if not word in word_count:
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1
    return word_count

def countWordIntoDocs(dico, docno, posting):
    for word, frequence in dico.items():
        posting.setdefault(word,[]).append((docno,frequence)) ### Remplace les lignes de commande suivante:
        """
        if not word in list(posting.keys()):
            posting[word] = [(docname, frequence)]
        else:
            posting[word].append((docname, frequence))
        """
    return posting

## Fonction de traintement du texte
def xml_text_minings(list_terms = dict(), use_stem=bool(), use_stopword=bool()):
    start = time.time()
    new_list_terms = {}
    posting_list = {}
    dl = list()
    for id, content in list_terms.items():
        text_clean = clean(content, use_stem, use_stopword)
        new_list_terms[id] = text_clean.split()  # Here we create a dictionary of Here we create a dictionary of
        # each docments with its terms
        lt = text_clean.split()
        current_dico = countWord(lt)
        posting_list = countWordIntoDocs(current_dico, id, posting_list)
    return posting_list, new_list_terms, (time.time() - start)

## Fonction de traintement du texte
def text_mining(fileName, use_stem=bool(), use_stopword=bool()):
    list_terms = {}
    docListNum, list_doc = preprocesDataFile(fileName)
    start = time.time()
    posting_list = {}
    file_number = fileName.split('/')[1].split('-', 1)
    dl = list()
    for i in range(len(list_doc)):
        text_clean = clean(docListNum[i][1], use_stem, use_stopword)
        list_terms[list_doc[i]] = text_clean.split()  # Here we create a dictionary of Here we create a dictionary of
        # each docments with its terms
        lt = text_clean.split()
        current_dico = countWord(lt)
        posting_list = countWordIntoDocs(current_dico, list_doc[i], posting_list)
    # tf = term_len(posting_list)
    # file_indexing_infos=(round(elapsed,3),tf)
    return posting_list, list_terms, (time.time() - start)


def get_statistics(posting_list, list_terms):
    stat = {}
    # document length
    stat['df'] = doc_len(list_terms)
    # Number of a doc
    stat['n_doc'] = len(stat['df'])
    # term length
    stat['tl'] = term_len(posting_list)
    # vocabulary size
    stat['voc_size'] = vocabulary_size(posting_list)
    # collection frequency of terms
    stat['colec_freq'] = collection_term_freq(posting_list)
    return stat