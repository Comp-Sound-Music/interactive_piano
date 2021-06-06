import tkinter as tk
import simpleaudio as sa # to play sound
import scipy.io.wavfile as wav # to write/read wavfiles
import numpy as np
from conversion_table import name_to_key
from itertools import cycle


# pressed_key = None
recording = False
recorded_keys = [] # maybe stupid


# generates sine samples
def create_sine(ampl, ss, sr, freq, t, ch=1):
    samples = np.linspace(0, t, int(t*sr), endpoint=False)  # generate samples
    sin = np.sin(2 * np.pi * freq * samples) # create sine wave
    wave = ampl * sin * (2**(ss - 1)) / np.max(np.abs(sin))
    wave = wave.astype(np.int16)
    #print(f'{wave} len: {len(wave)}',f'\nmax: {np.max(wave)}  min: {np.min(wave)}')
    return wave


'''
        purpose: 
            * This function opens the file passed in as a parameter and plays it
        args:
            * filename: name of file to be open and played
        returns: 
            * Success: (samplerate,data)  ==> sample rate is just len(dara)
            * Failure: None
'''
'''
def open_file(filename='sounds/sine.wav'):

    try:
        print(f'reading {filename}...')
        samplerate,data = wav.read(filename=filename) # read file name
        return (samplerate,data) 
    except Exception as e:
        print(e)
    return None
'''


# plays the resulting harmony waveform
def play_harmonies(sound):
    play_obj = sa.play_buffer(sound, 1, 2, samp_rt)
    play_obj.wait_done()


def play_sound(sound, key_name):
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
            samplerate = len(sound)
            play_obj = sa.play_buffer(sound, 1, 2, samplerate)
            play_obj.wait_done()
            global recording
            if recording:
                recorded_keys.append(key_name) # add pressed key to list
            return True
        except Exception as e:
            print(e)
        return False
    return call_back


'''
def press_key(key,fun):
    pressed_key = key
    fun() # invoke fun
    return
'''


# get frequency from MIDI value
def midi_to_freq(note):
    a = 440  # frequency of A4
    return (a / 32) * (2 ** ((note - 9) / 12))


# calculate harmonies from pressed keys
def create_harmonies(keys):
    step_third = 4
    step_fifth = 7
    root_freqs = []
    third_freqs = []
    fifth_freqs = []
    # get the harmony frequencies
    for x in keys:
        l = names.index(x)
        root_freqs.append(note_frequency[l])
        key_midi_val = name_to_key[x]
        third_rel_step = (key_midi_val - 60) + step_third
        fifth_rel_step = (key_midi_val - 60) + step_fifth
        if third_rel_step < 12:
            calc = midi_to_freq(key_midi_val + step_third)
            third_freqs.append(calc)
        else:
            x = third_rel_step - 12
            calc = midi_to_freq(60 + x)
            third_freqs.append(calc)
        if fifth_rel_step < 12:
            calc = midi_to_freq(key_midi_val + step_fifth)
            fifth_freqs.append(calc)
        else:
            x = fifth_rel_step - 12
            calc = midi_to_freq(60 + x)
            fifth_freqs.append(calc)
    # create sample waves for harmony notes
    root_waves = np.zeros((len(keys), samp_rt))
    third_waves = np.zeros((len(keys), samp_rt))
    fifth_waves = np.zeros((len(keys), samp_rt))
    for x in range(len(keys)):
        root_waves[x] = create_sine(amp, samp_sz, samp_rt, root_freqs[x], t)
        third_waves[x] = create_sine(amp, samp_sz, samp_rt, third_freqs[x], t)
        fifth_waves[x] = create_sine(amp, samp_sz, samp_rt, fifth_freqs[x], t)
    root_waves = root_waves.astype(np.int16)
    third_waves = third_waves.astype(np.int16)
    fifth_waves = fifth_waves.astype(np.int16)
    # add harmony waves together and play result
    harmony_waves = np.add(root_waves, third_waves)
    harmony_waves = np.add(harmony_waves, fifth_waves)
    harmony_waves = np.reshape(harmony_waves, (len(keys) * samp_rt))
    harmony_waves = harmony_waves.astype(np.int16)
    play_harmonies(harmony_waves)


#  updates the recording global to indicate a recording state
def record(event):
    global recording
    if recording == True:
        print("stopped recording!")
        recording = False
        create_harmonies(recorded_keys)
        return
    print("starting recording ....")
    recorded_keys.clear()
    recording = True
    return

'''
def release_key(event):
    # don't like this even if it was member variable
    # pressed_key = None
    print('released: {}',event)
    return
'''


#  creates individual keys on the piano GUI
def create_key(root, text, note, fg="black", bg="white", w=5, h=10, bw=5):
    button = tk.Button(root,
                text=text,
                foreground = fg,
                background = bg,
                width=w,
                heigh=h,
                anchor='s',
                borderwidth=bw)
    button.bind('<ButtonPress>', play_sound(note, text))  # pass note & text (will be recorded in play_sound)
    return button


#  creates the piano GUI
def create_piano(root, notes):
    # split notes on keys (blacks vs whites)
    wkeys = list(filter(lambda x: not x[-1].endswith("b"), notes))
    bkeys = list(filter(lambda x: x[-1].endswith("b"), notes))
    
    w = 5
    h = 8
    # create white keys
    for k in range(len(wkeys)):
        key = wkeys[k][-1]
        note = wkeys[k][0]
        b = create_key(root, key, note, w=w, h=h*2, bw=2)
        b.grid(row=0, column=k, sticky='n')
    # create black keys
    for k in range(len(bkeys)):
        note = bkeys[k][0]
        key = bkeys[k][-1]
        b = create_key(root, key, note, w=w-2, h=h, fg="white", bg="black")
        if k >= 2:
            k += 1
        b.grid(row=0, column=k, columnspan=2, sticky='n')
    return


window = tk.Tk()
window.title("Play something!")

amp = 0.25
samp_sz = 16
samp_rt = 48000
f = 440
t = 1

#  frequencies for one Octave:
note_frequency = \
    np.array([523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77, 1046.50])
#               C5     Db       D       Eb      E       F      Gb       G       Ab      A       Bb      B       C6

#  Sine waves for each note
notes = np.empty((13, 48000))
for i in range(13):
    notes[i] = (create_sine(amp, samp_sz, samp_rt, note_frequency[i], t))

# need to map the notes correctly to the displayed keys (black kes vs white keys)
# build a dict with the note names
names = ["C5", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B", "C6"]
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
rec.bind('<ButtonPress>', record)  # row = 0, key = k

rec.grid(row=3, column=0, sticky='n')

window.mainloop()
