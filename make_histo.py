import pandas as pd
import json

parsed = pd.read_csv('data.csv', low_memory=False, index_col=0)

def ind_to_string(ind):
    if ind >= 10:
        return str(ind)
    else:
        return ' ' + str(ind)

def make_edu_hist():
    e_v = parsed['Education'].value_counts()

    edu = {
    1: 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0
    }

    ind_did_not_finish_hs = [i for i in range(12)] + [31, 32]
    ind_finished_hs_or_GED = [12, 21]
    ind_some_college = [i for i in range(13, 16)] + [34]
    ind_finished_college = [16, 23, 35]
    ind_finished_grad_school = [24]
    ind_trade_or_vocational = [22, 33]

    for ind in ind_did_not_finish_hs:
        edu[1] += e_v[ind_to_string(ind)]

    for ind in ind_finished_hs_or_GED:
        edu[2] += e_v[ind_to_string(ind)]

    for ind in ind_some_college:
       edu[3] += e_v[ind_to_string(ind)]

    for ind in ind_finished_college:
       edu[4] += e_v[ind_to_string(ind)]

    for ind in ind_finished_grad_school:
        edu[5] += e_v[ind_to_string(ind)]

    for ind in ind_trade_or_vocational:
       edu[6] += e_v[ind_to_string(ind)]

    return pd.Series(edu)

def make_gender_hist():
    g_h = parsed['Gender'].value_counts()
    del g_h[' ']
    return g_h

def make_race_hist():
    r_h = parsed['Race'].value_counts()
    del r_h[' ']
    r_h['9'] *= 5
    return r_h

def make_ms_hist():
    ms_h = parsed['Marital Status'].value_counts()
    del ms_h[' ']
    return ms_h

def make_prior_hist():
    with open('hists.txt', 'r') as f:
        a = json.loads(f.readline())
        return pd.Series(sorted(a[0].items(), key=lambda x: x[1], reverse=True))[:5], pd.Series(sorted(a[1].items(), key=lambda x: x[1], reverse=True))[:4], pd.Series(sorted(a[2].items(), key=lambda x: x[1], reverse=True))[:5], pd.Series(sorted(a[3].items(), key=lambda x: x[1], reverse=True))