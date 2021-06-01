'''
    This is just a script to play around with tkinter and try creating trashy versions of our project
'''
import tkinter as tk
import simpleaudio as sa # to play sound
import scipy.io.wavfile as wav # to write/read wavfiles
import numpy as np
from pychord import Chord
from itertools import cycle


# pressed_key = None
recording = False
recorded_keys = [] # maybe stupid


def create_sine(ampl,ss,sr,freq,t,ch = 1):
    '''
        generates a wave sound (will probably get rid of this) it makes incorrect samples
    '''
    samples = np.linspace(0, t, int(t*sr), endpoint = False) # generate samples 
    sin =  np.sin(2 * np.pi * freq * samples) # create sine wave
    wave = ampl * sin * (2**(ss - 1)) / np.max(np.abs(sin))
    wave = wave.astype(np.int16)
    #print(f'{wave} len: {len(wave)}',f'\nmax: {np.max(wave)}  min: {np.min(wave)}')
    return wave

def open_file(filename='sounds/sine.wav'):
    '''
        purpose: 
            * This function opens the file passed in as a parameter and plays it
        args:
            * filename: name of file to be open and played
        returns: 
            * Success: (samplerate,data)  ==> sample rate is just len(dara)
            * Failure: None
    '''
    try:
        print(f'reading {filename}...')
        samplerate,data = wav.read(filename=filename) # read file name
        return (samplerate,data) 
    except Exception as e:
        print(e)
    return None



def play_sound(sound,key_name):
    '''
        purpose: 
            * plays the passed wave sound
        args:
            * sound: a tuple of (wave sound, name of note)
        returns: 
            * curreid function
    '''
    def call_back(e):
        try:
            print(e)
            #samplerate,data = wav.read(filename=filename) # read file name
            samplerate = len(sound)
            play_obj = sa.play_buffer(sound, 1, 2, samplerate)
            play_obj.wait_done()
            global recording
            if recording:
                recorded_keys.append(key_name) # for now only record name of keys pressed
            # add key to the recording
            return True
        except Exception as e:
            print(e)
        return False
    return call_back

# def press_key(key,fun):
#     pressed_key = key
#     fun() # invoke fun
#     return

def record(event):
    '''
        This function updates the recording global to indicate a recording state
    '''
    global recording
    if recording == True:
        print("stopped recroding!") 
        print(recorded_keys)
        recording = False
        return
    print("starting recroding ....")
    # should we clear the recording (in case recording stopped and now we are recording something new)
    recording = True
    return

def release_key(event):
    # don't like this even if it was member variable
    # pressed_key = None
    print('released: {}',event)
    return

def create_key(root,text,note,fg="black",bg="white",w=5,h=10,bw=5):
    '''
        creates a key in the piano (tk button) with the given params
    '''
    button = tk.Button(root,
                text=text,
                foreground = fg,
                background = bg,
                width=w,
                heigh=h,
                anchor='s',
                borderwidth=bw)
    button.bind('<ButtonPress>',play_sound(note,text)) # pass note & text (will be recorded in play_sound)
    return button
def create_piano(root,notes):
    '''
        this function creates white & black keys
    '''
    # split notes on keys (blacks vs whites)
    wkeys = list(filter(lambda x: not x[-1].endswith("b"),notes))
    bkeys = list(filter(lambda x: x[-1].endswith("b"),notes))
    
    w = 5
    h = 8
    # create white keys
    for k in range(len(wkeys)):
        key = wkeys[k][-1]
        note = wkeys[k][0]
        b = create_key(root,key,note,w=w,h=h*2,bw=2)
        b.grid(row=0, column=k, sticky='n')
    # create black keys
    for k in range(len(bkeys)):
        note = bkeys[k][0]
        key = bkeys[k][-1]
        b = create_key(root,key,note,w=w-2,h=h,fg="white",bg="black")
        if k >= 2:
            k += 1
        b.grid(row=0, column=k, columnspan=2, sticky='n')
    return



window = tk.Tk()
window.title("very trashy interactive keyboard")

amp = 0.25
samp_sz = 16
samp_rt = 48000
f = 440
t = 1

#  Frequency of notes:
#  https://en.wikipedia.org/wiki/Piano_key_frequencies

#  frequencies for one Octave:
note_frequency = \
    np.array([261.6, 277.18, 293.665, 311.1, 329.63, 349.2, 369.99, 391.99, 415.3, 440.0, 466.16, 493.88, 523.25])
#               C4     Db       D       Eb     E       F      Gb      G       Ab     A      Bb      B       C5

#  Sine waves for each note
notes = np.empty((13, 48000))
for i in range(13):
    notes[i] = (create_sine(amp, samp_sz, samp_rt, note_frequency[i], t))

# need to map the notes correctly to the displayed keys (black kes vs white keys)
# building a dict using the following order: C4     Db       D       Eb     E       F      Gb      G       Ab     A      Bb      B       C5
names = ["C4","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B","C5"]

notes = notes.astype(int)
zipped_notes = list(zip(notes,names))
create_piano(window, zipped_notes)

# add the recording button:
rec = tk.Button(
    window,
    text="record",
    background="red",
    foreground="white"
    )
rec.bind('<ButtonPress>',record) # row = 0, key = k

rec.grid(row = 3, column=0,sticky='n')

window.mainloop()
