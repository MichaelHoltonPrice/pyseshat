import pandas as pd
import pkg_resources
import os

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
 