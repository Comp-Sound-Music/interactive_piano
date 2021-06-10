import unittest
import numpy as np
from scipy import fftpack
from piano import create_harmonies
from conversion_table import name_to_key as table

class CreateHarmonies(unittest.TestCase):
    def test_create_harmonies(self):
        # reference (with permission): https://cs510sound-spring2021.zulip.cs.pdx.edu/#narrow/stream/7-general/topic/HW.203.3A.20Chord.3F/near/2239
        samp_rt = 48000
        eps = 2.
        act_freqs = [ 
            523.25,
            554.37,
            587.33,
            622.25,
            659.26,
            698.46,
            739.99,
            783.99,
            830.61,
            880.0,
            932.33,
            987.77,
            1046.5
        ]
        for i,k in enumerate(table.keys()):
            v = table[k]
            ret = create_harmonies([k])
            x = fftpack.fft(ret)
            freqs = fftpack.fftfreq(len(x)) * samp_rt
            peaks = np.argsort(np.abs(x))[-6:]
            peak = round(np.sort(freqs[peaks])[-1],2)
            diff = round(np.abs(peak-act_freqs[i]),2)
            print(f"Test {k}  -- |{peak} - {act_freqs[i]}| = {diff}")
            self.assertTrue(diff <= eps)
        return

if __name__=="__main__":
    unittest.main()
