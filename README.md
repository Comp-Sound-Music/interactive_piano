## CS 410/510 Course Project
**Group Members: Stephanie Beagle (beagle@pdx.edu), Mohammed Alsaid (alsaid@pdx.edu), Nhan Le (email here)**

Our idea for the project was to build an interactive piano interface that allows the user to play and record melodies and the program would add harmonies to it.  
We built the piano GUI using **tkinter** and mapped each of the keys to a specific note between C5 and C6. We used the **simpleaudio** library to play the audio directly from the waveform samples to avoid having to write and read wav files.  
When the user presses the record button, the program records each key press and stores the note names in a list. When the recording is finished, a function calculates the relative frequencies of the third and fifth
of each note pressed and creates waveforms for each one. Similar to the assignment in homework 3, the waveforms are then added together to create a chord and the user's melody is played back with the added harmonies.  
To verify our output we wrote test scripts to validate that the program produces accurate frequency calculations, correct waveforms, and correct note selection (see tests section below).  
If we had more time to work on the project, we would have liked to implement support for overlapping notes and different note timing, but unfortunately we weren't able to get a working version of that before the due date. 



## Creating virtual env (optional):
__Create env__: `python3 -m venv vev`

__Activate env__: `source venv/bin/activate`

## Install requirements:
__run__: `pip3 install -r reqs.txt`

## Run program:
`python3 piano.py`

## Tests:
run all tests: `python3 -m unittest tests/all.py`

run specific test: `python3 -m unittest tests/test_specific.py`

## Notes:
__under arch__: installing tkinter (`tk`) using pip might not be enough. Use `sudo pacman -Syu tk` to install tkinter.
