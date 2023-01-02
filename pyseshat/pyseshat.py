import pandas as pd
import pkg_resources
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
import copy

def tailoredSvd(data):
    """A util method to call numpy to do an SVD after removing the mean
    """
    data -= np.mean(data, axis=0)
    P, D, Q = np.linalg.svd(data, full_matrices=False)
    PC_matrix = np.matmul(data, Q.T)
    return P, D, Q, PC_matrix

def loadPNAS2017CC(scale=False):
    """Load the CC data from the 2017 PNAS article. Both the array and CC names
    are returned.

    Keyword arguments:
    scale -- Whether to scale the CC array (default False, do not scale)
    """
    CC_df = loadSeshatDataset(version='PNAS2017', flavor='Imputations')
    CC_names = ['PolPop','PolTerr', 'CapPop',
                'levels', 'government','infrastr',
                'writing', 'texts', 'money']
    CC_array = CC_df.loc[:, CC_names].values
    if scale:
        CC_array = StandardScaler().fit_transform(CC_array)
    return CC_array, CC_names
 
def loadSeshatDataset(version, flavor=None):
    """Load a seshat dataset

    Keyword arguments:
    version -- The version of the dataset ('PNAS2017' or 'Equinox')
    flavor -- For 'Equinox', the worksheet.
    """

    # Do error checking
    if not version in ['PNAS2017', 'Equinox']:
        raise ValueError('Unrecognized version = ' + version)
    
    data_dir = pkg_resources.resource_filename('pyseshat', 'data/')
    if version == 'Equinox':
        if flavor is None:
            raise TypeError('flavor (worksheet) must be specified for the\
                Equinox dataset')

        worksheets = getEquinoxWorksheets()
        if not flavor in worksheets:
            raise ValueError('Unrecognized Equinox worksheet (flavor) = '\
                 + flavor)

        file_path = os.path.join(data_dir, 'Equinox_on_GitHub_June9_2022.xlsx')
        return pd.read_excel(file_path, sheet_name=flavor)

    if version == 'PNAS2017':
        if flavor is None:
            raise TypeError('flavor (Imputations or PCs) must be specified for\
                the PNAS2017 dataset')

        if not flavor in ['Imputations', 'PCs']:
            raise ValueError('For PNAS2017, the flavor must be Imputations or\
                PCs')

        if flavor == 'Imputations':
            file_name = 'data1.csv'
        elif flavor == 'PCs':
            file_name = 'data1.csv'
        else:
            raise Exception('This should not happen')
        file_path = os.path.join(data_dir, file_name)
        return pd.read_csv(file_path)

def getEquinoxWorksheets():
    """A utility function for getting the worksheets in the Equinox Excel file
    """
    return ['Metadata',
            'Equinox2020_CanonDat',
            'CavIronHSData',
            'HistYield+',
            'TSDat123',
            'AggrSCWarAgriRelig',
            'ImpSCDat',
            'SPC_MilTech',
            'Polities',
            'Variables',
            'NGAs',
            'Scale_MI',
            'Class_MI']
 
def getRegionDict(version):
    """Get a dictionary where the key is the region (e.g., 'Africa') and the
    entries are lists of NGAs

    Keyword arguments:
    version -- Which version is this for? e.g., PNAS2017 or Equinox
    """

    # There are any number of ways this method could be implemented. I have
    # chosen to simply create the full regionDict directly for each case.
    regionDict = dict()

    if version == 'Equinox':
        regionDict["Africa"] =\
            ["Ghanaian Coast",
             "Niger Inland Delta",
             "Upper Egypt"]
        regionDict["Europe"] =\
            ["Iceland",
             "Crete", # new
             "Latium",
             "Paris Basin"]
        regionDict["Central Eurasia"] =\
            ["Lena River Valley",
             "Orkhon Valley",
             "Sogdiana"]
        regionDict["Southwest Asia"] =\
            ["Galilee", # new
             "Konya Plain",
             "Southern Mesopotamia", # new
             "Susiana",
             "Yemeni Coastal Plain"]
        regionDict["South Asia"] =\
            ["Garo Hills",
             "Deccan",
             "Kachi Plain",
             "Middle Ganga"] # new
        regionDict["Southeast Asia"] =\
            ["Cambodian Basin",
             "Central Java",
             "Kapuasi Basin"]
        regionDict["East Asia"] =\
            ["Kansai",
             "Southern China Hills",
             "Middle Yellow River Valley"]
        regionDict["North America"] =\
            ["Cahokia",
             "Basin of Mexico", # new
             "Finger Lakes",
             "Valley of Oaxaca"]
        regionDict["South America"] =\
            ["Cuzco",
             "Lowland Andes",
             "North Colombia"]
        regionDict["Oceania-Australia"] =\
            ["Big Island Hawaii",
             "Chuuk Islands",
             "Oro PNG"]
    elif version == 'PNAS2017':
        regionDict["Africa"] =\
            ["Ghanaian Coast",
             "Niger Inland Delta",
             "Upper Egypt"]
        regionDict["Europe"] =\
            ["Iceland",
             "Latium",
             "Paris Basin"]
        regionDict["Central Eurasia"] =\
            ["Lena River Valley",
             "Orkhon Valley",
             "Sogdiana"]
        regionDict["Southwest Asia"] =\
            ["Konya Plain",
             "Susiana",
             "Yemeni Coastal Plain"]
        regionDict["South Asia"] =\
            ["Garo Hills",
             "Deccan",
             "Kachi Plain"]
        regionDict["Southeast Asia"] =\
            ["Cambodian Basin",
             "Central Java",
             "Kapuasi Basin"]
        regionDict["East Asia"] =\
            ["Kansai",
             "Southern China Hills",
             "Middle Yellow River Valley"]
        regionDict["North America"] =\
            ["Cahokia",
             "Finger Lakes",
             "Valley of Oaxaca"]
        regionDict["South America"] =\
            ["Cuzco",
             "Lowland Andes",
             "North Colombia"]
        regionDict["Oceania-Australia"] =\
            ["Big Island Hawaii",
             "Chuuk Islands",
             "Oro PNG"]
    else:
        raise ValueError('Unrecognized version = ' + version)
    return regionDict
 
def getNGAs(version):
    """Get a list of all NGAs.

    Keyword arguments:
    version -- Which version is this for? e.g., PNAS2017 or Equinox
    """
    # The core functionality is in getRegionDict
    regionDict = getRegionDict(version)
    NGAs = list()
    for key in regionDict.keys():
        for nga in regionDict[key]:
            NGAs.append(nga)
    
    NGAs.sort()
    return NGAs
