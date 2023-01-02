import unittest
from pyseshat.pyseshat import *
import math

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

    def test_loadPNAS2017CC(self):
        # Check that we can load both the unscaled and scaled CC arrays
        CC_array_unscaled, _ = loadPNAS2017CC()
        self.assertEqual(CC_array_unscaled.shape, (8280, 9))
        CC_array_scaled, _ = loadPNAS2017CC(scale=True)
        self.assertEqual(CC_array_scaled.shape, (8280, 9))

        # Iterate over columns to check the scaling
        for cc_num in range(9):
            CC_unscaled = CC_array_unscaled[:,cc_num]
            self.assertNotAlmostEqual(np.mean(CC_unscaled), 0, places=8)
            self.assertNotAlmostEqual(np.std(CC_unscaled), 1, places=8)
            CC_scaled = CC_array_scaled[:,cc_num]
            self.assertAlmostEqual(np.mean(CC_scaled), 0, places=8)
            self.assertAlmostEqual(np.std(CC_scaled), 1, places=8)

            CC_rescaled = CC_unscaled - np.mean(CC_unscaled)
            CC_rescaled = CC_rescaled / np.std(CC_rescaled)
            # TODO: there most be a better way to check equality for vectors
            for i in range(len(CC_rescaled)):
                self.assertAlmostEqual(CC_scaled[i], CC_rescaled[i], places=8)

    def test_getRegionDict(self):
        # Ensure an error is thrown for an unsupported version
        with self.assertRaises(ValueError):
            _ = getRegionDict(version='Bad Version')

        # Check the regionDict for Equinox
        regionDict = getRegionDict('Equinox')
        self.assertEqual(len(regionDict), 10)
        self.assertEqual(len(regionDict['Africa']), 3)
        self.assertEqual(len(regionDict['Europe']), 4)
        self.assertEqual(len(regionDict['Central Eurasia']), 3)
        self.assertEqual(len(regionDict['Southwest Asia']), 5)
        self.assertEqual(len(regionDict['South Asia']), 4)
        self.assertEqual(len(regionDict['Southeast Asia']), 3)
        self.assertEqual(len(regionDict['East Asia']), 3)
        self.assertEqual(len(regionDict['North America']), 4)
        self.assertEqual(len(regionDict['South America']), 3)
        self.assertEqual(len(regionDict['Oceania-Australia']), 3)

        # Check the regionDict for PNAS2017 
        regionDict = getRegionDict('PNAS2017')
        self.assertEqual(len(regionDict), 10)
        for key in regionDict.keys():
            self.assertEqual(len(regionDict[key]), 3)

    def test_getNGAs(self):
        # Ensure an error is thrown for an unsupported version
        with self.assertRaises(ValueError):
            _ = getNGAs(version='Bad Version')

        # Check Equinox
        NGAs = getNGAs(version='Equinox')
        self.assertEqual(len(NGAs), 35)

        # Check PNAS2017 
        NGAs = getNGAs(version='PNAS2017')
        self.assertEqual(len(NGAs), 30)

    def test_tailoredSvd(self):
        # Do an SVD on the original PNAS 2017 dataset and check the variance
        # explained by PC1 (it should be .772)
        CC_matrix, _ = loadPNAS2017CC(scale=True)
        P, D, Q, PC_matrix = tailoredSvd(CC_matrix)
        Dsqr = [v**2 for v in D]
        PC1_var = Dsqr[0] / np.sum(Dsqr)
        self.assertAlmostEqual(PC1_var, .772, places=3)

if __name__ == '__main__':
    unittest.main()