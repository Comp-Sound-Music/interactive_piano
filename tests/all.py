import unittest
# from tests.test_charger import TestCharger
from tests.test_create_sine import CreateSine
from tests.test_midi_to_freq import MidiToFreq
from tests.test_create_harmonies import CreateHarmonies

def suite():
    suite = unittest.TestSuite()
    suite.addTest(CreateSine('test create sine function'))
    suite.addTest(CreateSine('test create harmonies function'))
    suite.addTest(CreateSine('test midi to frequency function'))
    return suite

if __name__=="__main__":
    runner = unittest.TestRunner() # create suite
    runner.run(suite()) # run suite