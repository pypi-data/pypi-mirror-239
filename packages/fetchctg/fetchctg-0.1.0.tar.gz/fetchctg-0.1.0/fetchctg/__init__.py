""" This is a list of the utility functions that can help fetch 
    the safety data from clinical trials listed on clinicaltrials.gov
    when provided with nctid of the trial provided the results are
    posted on the clinicaltrials.gov portal. """

import pandas as pd
import numpy as np
import requests
import datetime
import json

def _decode_event_group(coded_value, event_group):
    """ Decode arm names, example - EG000 to 'Dupilumab 300 mg qw

    Parameters
    ----------
    coded_value : str
        The coded value we are trying to decode
    event_group : str
        The event group text coming from the clinical trial page on clinicaltrial.gov

    Returns
    -------
    string
        a description text with decoded value (if decoding fails then coded value is returned as is
    """
    decoded_value = event_group[event_group.EventGroupId==coded_value]['EventGroupTitle'].values[0]
    if not decoded_value:
        decoded_value = coded_value
    return decoded_value



def get_oae(nctid):
    """ This function returns other (non-serious) adverse events

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
    pandas DataFrame
        a table containing the detailed records of non-serious adverse events for each arm of the trial
    """

    # Get CT.gov data on the NCTID
    URL = f'https://clinicaltrials.gov/api/query/full_studies?expr={nctid}&max_rnk=1&fmt=JSON'
    r = requests.get(URL)
    j = json.loads(r.content)
    # Other AE data
    tt = j['FullStudiesResponse']['FullStudies'][0]['Study']['ResultsSection']['AdverseEventsModule']['OtherEventList']['OtherEvent']
    event_groups = pd.json_normalize(j['FullStudiesResponse']['FullStudies'][0]['Study']['ResultsSection']['AdverseEventsModule']['EventGroupList']['EventGroup'])
    # convert into tabular format
    tt2 = pd.json_normalize(tt,
              ['OtherEventStatsList','OtherEventStats'],
              ['OtherEventTerm', 'OtherEventOrganSystem'],
              errors='ignore')
    # In rare cases there could be multiple entries for a single arm + Event Term e.g.NCT01425281
    tt2 = tt2.drop_duplicates(subset=['OtherEventStatsGroupId',                                  
                                  'OtherEventStatsNumAtRisk',
                                  'OtherEventTerm'], keep='last')
    # convert into multi-indexed column
    try:
        tt2 = tt2.drop_duplicates(subset=['OtherEventStatsGroupId','OtherEventStatsNumAffected','OtherEventStatsNumEvents','OtherEventStatsNumAtRisk','OtherEventTerm'])
        tt3 = tt2.pivot(columns='OtherEventStatsGroupId',
        values=['OtherEventStatsNumAffected','OtherEventStatsNumEvents','OtherEventStatsNumAtRisk'],
        index='OtherEventTerm')
        tt3.rename(columns={'OtherEventStatsNumEvents':'Events'}, inplace=True, level=0)
    except KeyError:
        tt3 = tt2.pivot(columns='OtherEventStatsGroupId',
        values=['OtherEventStatsNumAffected','OtherEventStatsNumAtRisk'],
        index='OtherEventTerm')
    tt3.rename(columns=lambda x: _decode_event_group(x,event_groups), inplace=True, level=1)
    tt3.rename(columns={'OtherEventStatsNumAffected':'Subjects','OtherEventStatsNumAtRisk':'Total_Subjects'}, inplace=True, level=0)
    return(tt3)



def get_sae(nctid):
    """ This function returns serious adverse events

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
    pandas DataFrame
        a table containing the detailed records of serious adverse events for each arm of the trial
    """

    # Get CT.gov data on the NCTID
    URL = f'https://clinicaltrials.gov/api/query/full_studies?expr={nctid}&max_rnk=1&fmt=JSON'
    r = requests.get(URL)
    j = json.loads(r.content)
    # Other AE data
    tt = j['FullStudiesResponse']['FullStudies'][0]['Study']['ResultsSection']['AdverseEventsModule']['SeriousEventList']['SeriousEvent']
    event_groups = pd.json_normalize(j['FullStudiesResponse']['FullStudies'][0]['Study']['ResultsSection']['AdverseEventsModule']['EventGroupList']['EventGroup'])
    # convert into tabular format
    tt2 = pd.json_normalize(tt,
              ['SeriousEventStatsList','SeriousEventStats'],
              ['SeriousEventTerm', 'SeriousEventOrganSystem'],
              errors='ignore')
    # In rare cases there could be multiple entries for a single arm + Event Term e.g NCT01425281
    tt2 = tt2.drop_duplicates(subset=['SeriousEventStatsGroupId',                                  
                                  'SeriousEventStatsNumAtRisk',
                                  'SeriousEventTerm'], keep='last')
    # convert into multi-indexed column
    try:
        tt3 = tt2.pivot(columns='SeriousEventStatsGroupId',
                    values=['SeriousEventStatsNumAffected','SeriousEventStatsNumEvents','SeriousEventStatsNumAtRisk'],
                    index='SeriousEventTerm')
        tt3.rename(columns={'SeriousEventStatsNumEvents':'Events'}, inplace=True, level=0)
    except KeyError:
        tt3 = tt2.pivot(columns='SeriousEventStatsGroupId',
                    values=['SeriousEventStatsNumAffected','SeriousEventStatsNumAtRisk'],
                    index='SeriousEventTerm')
    tt3.rename(columns=lambda x: _decode_event_group(x,event_groups), inplace=True, level=1)
    tt3.rename(columns={'SeriousEventStatsNumAffected':'Subjects','SeriousEventStatsNumAtRisk':'Total_Subjects'}, inplace=True, level=0)
    return(tt3)


def get_ae_summary(nctid):
    # Get CT.gov data on the NCTID
    URL = f'https://clinicaltrials.gov/api/query/full_studies?expr={nctid}&max_rnk=1&fmt=JSON'
    r = requests.get(URL)
    j = json.loads(r.content)
    tt = pd.json_normalize(j['FullStudiesResponse']['FullStudies'][0]['Study']['ResultsSection']['AdverseEventsModule']['EventGroupList']['EventGroup'])
    for cols in ['EventGroupSeriousNumAffected', 'EventGroupSeriousNumAtRisk', 'EventGroupOtherNumAffected']:
        tt[cols] = tt[cols].apply(pd.to_numeric, errors='coerce')
    return tt.sum(axis = 0, skipna = True, numeric_only = True) 


def get_all_ae(nctid):
    """ This function returns all (serious and non-serious) adverse events

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
    dict
        a dictionary with 2 pandas DataFrame containing the detailed records of serious 
        and non-serious adverse events for each arm of the clinical trial
    """


    sae = get_se(nctid)
    oae = get_oae(nctid)
    return {"sae": sae, "oae": oae} 


def save_sae(nctid):
    """ This function saves serious adverse events in an excel file

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
        NA
    """
    sae = get_sae(nctid)
    sae.to_excel(f"{nctid}_sae.xlsx")
    return


def save_oae(nctid):
    """ This function saves other (non-serious) adverse events in an excel file

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
        NA
    """
    oae = get_oae(nctid)
    oae.to_excel(f"{nctid}_oae.xlsx")
    return


def save_all_ae(nctid):
    """ This function saves all (serious and non-serious) adverse events in 
        two different sheets of an excel file

    Parameters
    ----------
    nctid: str
        The alphnumeric value (starts with N) associated with a registered trial

    Returns
    -------
        NA
    """
    sae = get_sae(nctid)
    oae = get_oae(nctid)
    with pd.ExcelWriter(f'{nctid}_all_ae.xlsx') as writer:  
        sae.to_excel(writer, sheet_name=f'{nctid}_sae')
        oae.to_excel(writer, sheet_name=f'{nctid}_oae')
    return

