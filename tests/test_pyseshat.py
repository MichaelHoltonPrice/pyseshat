import unittest
from pyseshat.pyseshat import *

class TestPyseshat(unittest.TestCase):

    def test_loadSeshatDataset(self):
        # Ensure an error is thrown for an unsupported version
        with self.assertRaises(ValueError):
            _ = loadSeshatDataset(version='Bad Version')

        # Error check the Equinox dataset
        with self.assertRaises(TypeError):
            _ = loadSeshatDataset(version='Equinox', flavor=None)

        with self.assertRaises(ValueError):
            _ = loadSeshatDataset(version='Equinox', flavor='Bad Worksheet')
        
        for worksheet in getEquinoxWorksheets():
            df = loadSeshatDataset(version='Equinox', flavor=worksheet)
            self.assertTrue(df.shape[0] > 0)

        # Error check the PNAS2017 dataset
        with self.assertRaises(TypeError):
            _ = loadSeshatDataset(version='PNAS2017', flavor=None)

        with self.assertRaises(ValueError):
            _ = loadSeshatDataset(version='Equinox', flavor='Bad Flavor')
        
        for flavor in ['Imputations', 'PCs']:
            df = loadSeshatDataset(version='PNAS2017', flavor=flavor)
            self.assertTrue(df.shape[0] > 0)

if __name__ == '__main__':
    unittest.main()