import math

def smart_ltn(posting_list,n, df_t):
    df = 0
    #(1+LOG(tf))*LOG(n/df)
    #tf is the frequence of term on a document
    #df number of document where the term appear
    ltn_value = {} # key doc number, value (terme, ltn)
    for term, value in posting_list.items():
        dl = df_t[term]
        df = dl[0][1] # nombre de doc dans lequel le terme apparait sur toute la collection
        for v in value:
            tf = v[1]
            ltn = (1+math.log10(tf))*(math.log10(n/df))
            ltn_value.setdefault(v[0],[]).append((term,round(ltn,4)))
    return ltn_value



def rsv_score(query, wf):
    rsv_doc = {}
    for term in query.split():
        for doc, values in wf.items():
            for v in values:
                if term == v[0]:
                    rsv_doc.setdefault(doc, []).append(v[1])
                else:
                    continue
    rsv = [(sum(wf_list), doc) for doc, wf_list in rsv_doc.items()]
    return rsv

def smart_ltc(smart_ltn):
    # ltn = doc:(term, ltn)
    #  (ltn_term/sqrt(sum(each pow(ltn_term,2))on a document))
    ltc_value = {}
    for doc, value in smart_ltn.items():
        pow_ltn_term = [pow(v[1],2) for v in value]
        normalize = math.sqrt(sum(pow_ltn_term))
        for v in value:
            ltc_value.setdefault(doc,[]).append((v[0],round((v[1]/normalize),4)))
    return ltc_value



def tf_part(posting_list,dl,n,k,b):
    #(tf*(k+1))/(k*((1-b)+b*(dl/avdl))+tf)
    #[  1     ]             [   2   ]
    #              [      3         ]
    #            [         4            ]
    dl_ = sum([dl[x] for x in dl.keys()])
    doc_len = 0
    avdl = dl_/n
    #print(avdl)
    #avdl = 20
    tf_part_val = {}
    for term, value in posting_list.items():
        for v in value:
            #if not term in v
            tf = v[1]
            doc_len = dl[v[0]]
            #doc_len = [doc_l for docno,doc_l in dl if docno==v[0]]
            bloc_1 = tf*(k+1)
            bloc_2 = doc_len/avdl
            bloc_3 = k * ((1-b) + b * bloc_2)
            bloc_4 = bloc_3+tf
            tf_part_val.setdefault(v[0],[]).append((term,bloc_1/bloc_4))
    return tf_part_val


def idf_part(posting_list,df_,n):
    #log((n-df+0.5)/(df+0.5))
    #    [   1    ] [  2   ]
    idf_part_val ={}
    for term, value in posting_list.items():
        df = df_[term]
        df = df[0][1]
        bloc_1 = abs(n-df+0.5)
        bloc_2 = df + 0.5
        idf_part_val.setdefault(term,[]).append(math.log10(bloc_1/bloc_2))
    return idf_part_val


def bm25(posting_list, stat):
    tf_part_ = tf_part(posting_list, stat['df'], stat['n_doc'])
    idf_part_ = idf_part(posting_list, stat['colec_freq'], stat['n_doc'])
    bm25_val = {}
    # doc 1 : ('a' , tf_part_[a]*idf[a])
    for doc, tf_value in tf_part_.items():
        for tf in tf_value:
            bm25_val.setdefault(doc, []).append((tf[0], tf[1] * idf_part_[tf[0]][0]))
    return bm25_val


def bm25(posting_list, stat,k,b):
    tf_part_ = tf_part(posting_list,stat['df'],stat['n_doc'],k,b)

    idf_part_ = idf_part(posting_list,stat['colec_freq'], stat['n_doc'])
    bm25_val = {}
    for doc, tf_value in tf_part_.items():
        for tf in tf_value:
            bm25_val.setdefault(doc,[]).append((tf[0], tf[1]*idf_part_[tf[0]][0]))     
    return bm25_val
    

def weinting_function(pl, stat,k,b):
    ltn = smart_ltn(pl,stat['n_doc'], stat['colec_freq'])
    ltc = smart_ltc(ltn)
    bm25_val = bm25(pl,stat,k,b)
   
    return ltn,ltc,bm25_val

def reverse_score(score_result):
    score = sorted(score_result, reverse=False)
    score = [(doc, result) for result, doc in score]
    return score
