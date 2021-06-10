import unittest
import numpy as np
from piano import create_sine
import matplotlib.pyplot as plt

class CreateSine(unittest.TestCase):
    def test_correct_wave(self):
        ampl = 1.
        freq = 440
        sr = 48000
        ss = 16
        t = 1.

        print(f'tesing create_sine...')
        r = np.linspace(0,t,int(t*sr),endpoint=False)
        samples = ampl*2**(ss-1) * np.sin(2 * np.pi * freq * r)
        samples = samples.astype(np.int16)
        ret_samples = create_sine(ampl,ss,sr,freq,t)
        for s,r in zip(samples,ret_samples):
            self.assertEqual(s,r)
        return

if __name__=="__main__":
    unittest.main()