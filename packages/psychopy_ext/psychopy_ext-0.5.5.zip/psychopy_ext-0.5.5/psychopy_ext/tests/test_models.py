import numpy as np
from .. import models

import unittest

class TestHMAX(unittest.TestCase):
    def test_gaussian(self):
        m = models.HMAX(matlab=True, filt_type='gaussian')
        out = m.run()
        fid = open('psychopy_ext/tests/lena_gaussian_matlab.txt')
        c2_matlab = np.array([float(i.strip('\n')) for i in fid.readlines()])
        c2_python = np.around(out['C2'], decimals=5)  # matlab's output has 5
                                                      # significant digits
        rms = np.mean(np.sqrt((c2_matlab - c2_python)**2))
        self.assertEqual(rms, 0)

    def test_gabor(self):
        m = models.HMAX(matlab=False, filt_type='gabor')
        out = m.run()
        fid = open('psychopy_ext/tests/lena_gabor_matlab.txt')
        c2_matlab = np.array([float(i.strip('\n')) for i in fid.readlines()])
        c2_python = np.around(out['C2'], decimals=5)  # matlab's output has 5
                                                      # significant digits
        rms = np.mean(np.sqrt((c2_matlab - c2_python)**2))
        self.assertEqual(rms, 0)


class TestGaborJets(unittest.TestCase):
    def setUp(self):
        m = models.GaborJet()
        self.mag, self.phase, self.grid = m.run(m.get_teststim())

    def test_mag(self):
        mag_matlab = np.genfromtxt('psychopy_ext/tests/jet_mag.txt', delimiter=',')
        mag_matlab = mag_matlab.ravel()
        mag_python = np.around(self.mag, decimals=5)  # matlab's output has 5
                                                      # significant digits
        mag_python = mag_python.ravel()
        rms = np.mean(np.sqrt((mag_matlab - mag_python)**2))
        self.assertTrue(rms, 0)

    def test_phase(self):
        phase_matlab = np.genfromtxt('psychopy_ext/tests/jet_phase.txt',
                                     delimiter=',')
        phase_matlab = phase_matlab.ravel()
        phase_python = np.around(self.mag, decimals=5) # matlab's output has 5
                                                       # significant digits
        phase_python = phase_python.ravel()
        rms = np.mean(np.sqrt((phase_matlab - phase_python)**2))
        self.assertTrue(rms, 0)


if __name__ == '__main__':
    unittest.main()
