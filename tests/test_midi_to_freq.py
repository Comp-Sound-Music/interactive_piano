import unittest
from piano import midi_to_freq
from conversion_table import name_to_key


class MidiToFreq(unittest.TestCase):
    def test_correct_freqs(self):
        # ref: https://newt.phys.unsw.edu.au/jw/notes.html 
        # hard coded frequencies
        freqs = [ 
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
        for i,k in enumerate(name_to_key.keys()):
            # print(f"{k} {v}")
            v = name_to_key[k]
            print(f"Test {k}")
            ret = midi_to_freq(v)
            self.assertEqual(freqs[i],round(ret,2))
        self.assertEqual(1,1)

if __name__=="__main__":
    unittest.main()