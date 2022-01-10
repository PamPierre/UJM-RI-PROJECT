import time

import random
from stop_words import get_stop_words
from weiting_function import *

def score(query_list,rsv_wf):
    team_name = "DjibrilMohamedOmaimaDouae"
    score = []
    for query in query_list:
        query = query.split(' ', 1)
        score.append(result_query(query[0], rsv_score(query[1], rsv_wf), team_name))
    return score

def result_query(num_query, rsv_result,team_name):
    start = time.time()
    score = reverse_score(rsv_result)
    x = score
    if len(x)>1500:
        x = x[:1500]
    rsv_r = [(num_query,
              'Q0', x[i][0],i+1,
              round(x[i][1],5), team_name,
              '/article[1]') for i in range(len(x))]
    return rsv_r


# wf_index is [0,1,2]==['ltn','ltc','bm25']
def create_run_file(run_id, wf_index, use_stem, use_stopword, k, b):
    run_directory = "../assets/runs_result/"
    run_id += 1
    team_name = "DjibrilMohamedOmaimaDouae"
    stem = ['nostem', 'porter', 'lovins', 'paice']
    wf = ['ltn', 'ltc', 'bm25']
    st = stem[0]
    sw = 'nostop'
    stopwords = get_stop_words('english')
    top = ''
    len_stop = ''
    if (use_stopword):
        sw = 'stop'
        len_stop = str(len(stopwords))
    if use_stem:
        st = stem[1]
        # name_Runid_wf_Granularity_use_Parameters.tx
    run_file_name = '{}_{}_{}_element_sec_p_{}{}_{}'.format(team_name, run_id,
                                                            wf[wf_index], sw,
                                                            len_stop, st)
    # Cas du bm25
    if (wf_index == 2):
        run_file_name = str(run_file_name + '_k{}_b{}'.format(k, b))

    run_file_path = str(run_directory + run_file_name + '.txt')
    return open(run_file_path, "w"), run_id


# index is [0,1,2]==['ltn','ltc','bm25']
def build_run_file(run_id, wf_score, index, use_stem, use_stopword, k, b):
    start = time.time()
    if index != 2:
        k = 0.0
        b = 0.0
    run_file_name, run_id = create_run_file(run_id, index, use_stem, use_stopword, k, b)
    print(len(wf_score))
    for score in wf_score:
        print(len(score))
        for i in range(len(score)):
            run_score = str(score[i]).replace(',', '').replace("'", '').replace('(', '').replace(')', '')
            run_file_name.write(run_score + "\n")
    run_file_name.close()

    print("Execution time for the run {} is {}".format(run_id, time.time() - start))
    return run_id


# uniquement pour le bm25tuning for a random value:
def bm25_tuning_random(run_id, number_run, score_bm25, use_stem, use_stopword):
    for i in range(number_run):
        k = random.uniform(1, 2)
        b = random.uniform(0.1, 1)
        run_id = build_run_file(run_id, score_bm25, 2, use_stem, use_stopword, k, b)
    print("Run number is {}".format(run_id))


# For the last exercise
def bm25_tuning(run_id, score_bm25, use_stem, use_stopword):
    start = time.time()
    k = 1.2
    b = 0.0
    for i in range(11):
        run_id = build_run_file(run_id, score_bm25, 2, use_stem, use_stopword, k, b)
        b += 0.1
    k = 0.0
    b = 0.75
    for i in range(21):
        run_id = build_run_file(run_id, score_bm25, 2, use_stem, use_stopword, k, b)
        k += 0.2

    print("Execution time for getting bm25_tuning is : {}".format(time.time() - start))
    print("Run number is {}".format(run_id))
