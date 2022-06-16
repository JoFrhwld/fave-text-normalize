import pympi
import re

def eaf_to_timing(elan_obj, tier_id):
    """
    Given an elan object, return a list of annotation tuples
    
    :param pympi.Elan.Eaf elan_obj: An elan object
    :param str tier_id: The tier to get
    """
    
    ts = elan_obj.timeslots
    annotations = elan_obj.tiers[tier_id][0]

    time_aligned = [(ts[annotations[key][0]]/1000,
                     ts[annotations[key][1]]/1000,
                     annotations[key][2]) 
                    for key in annotations]
    return(time_aligned)

def mispronounce(text, unk_mispronounce):
    """
    remove mispronunciation symbol
    """
    if unk_mispronounce == True:
        out = re.sub(r'\*\w+', "<unk>", text)
    else:
        out = text.replace("*", "")
    return(out)

def noises(text, unk_noise):
    """
    remove noise annotation
    """

    if unk_noise == True:
        out = re.sub(r'\{[A-Z][A-Z]\}', '<unk>', text)
    else:
        out = re.sub(r'\{[A-Z][A-Z]\}', '', text)
        out = rm_multispace(out)
    return(out)

def normalize_text(text, 
                   unk_uncertain = False, 
                   unk_partial = False, 
                   rm_restart = True, 
                   unk_mispronounce = False, 
                   unk_noise = False):
    """
    Given a text input, normalize it
    :param str text: text string to normalize
    :param unk_uncertain bool: convert uncertain annotations to <unk>
    :param unk_partial bool: convert partial words to <unk>
    :param rm_restart bool: remove restart symbols
    :param unk_mispronounced bool: convert mispronounced wordsto <unk>
    :param unk_noise bool: convert {NS}, {LG}, {BR}, {CG} to <unk> (default is to remove)
    """

    text = uncertain(text, unk_uncertain)
    text = partial(text, unk_partial)
    text = restart(text, rm_restart)
    text = mispronounce(text, unk_mispronounce)
    text = noises(text, unk_noise)

    return(text)

def partial(text, unk_partial=False):
    """
    remove partialword continuation
    """

    out = re.sub(r'\+\w+', '', text)
    out = rm_multispace(out)
    if unk_partial == True:
        out = re.sub(r'\w+-($|\W)', r"<unk>\1", out)
    return(out)

def restart(text, rm_restart = True):
    """
    remove the researt hesitation markers
    """

    if rm_restart == True:
        out = text.replace("--", "")
        out = rm_multispace(out)
    else:
        out = text
    
    return(out)

def rm_multispace(text):
    """
    remove multiple space
    """
    out = re.sub(r'\s+', " ", text).strip()
    return(out)

def uncertain(text, unk_uncertain=False):
    """
    Remove uncertain transcription
    """
    if unk_uncertain == True:
        out = re.sub(r'\(\(.*?\)\)', "<unk>", text)
    else:
        out = re.sub(r'\(\(|\)\)', "", text)
    return(out)