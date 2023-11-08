import pandas as pd

def get_data(path):
    pdcsv = pd.read_csv(path)
    return pdcsv

def get_grupos_pokemon(path):
    pdcsv = get_data(path)
    return pdcsv['type'].tolist()


def get_altura_media_grupo(path,type):
    pdcsv = get_data(path)
    result = pdcsv[pdcsv['type'] == type]['height']
    return result

def get_peso_media_grupo(path,type):
    pdcsv = get_data(path)
    result = pdcsv[pdcsv['type'] == type]['weight']
    return result

