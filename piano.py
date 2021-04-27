'''
    This is just a script to play around with tkinter and try creating trashy versions of our project
'''
import tkinter as tk
import simpleaudio as sa # to play sound
import scipy.io.wavfile as wav # to write/read wavfiles
import numpy as np
from pychord import Chord


pressed_key = None


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




def play_sound(sound):
    '''
        purpose: 
            * plays the passed wave sound
        args:
            * sound: a wave sound
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
            return True
        except Exception as e:
            print(e)
        return False
    return call_back

# def press_key(key,fun):
#     pressed_key = key
#     fun() # invoke fun
#     return

def release_key(event):
    # don't like this even if it was member variable
    # pressed_key = None
    print('released: {}',event)
    return

def create_piano(root,sounds,keys=12):
    '''
        this function creates white & black keys (shitty version)
    '''
    w = 5
    h = 10
    # create white keys
    for k in range(keys):
        b = tk.Button(root,#text = f'key:{k}',
                borderwidth=5,
                width=w,
                height=h*2)
        b.bind('<ButtonPress>',play_sound(sounds[k])) # row = 0, key = k
        # b.bind('<ButtonRelease>',release_key)
        b.grid(row=0, column=k, sticky='n')
    # create black keys
    for k in range(keys-1):
        b = tk.Button(root,#text = f'key:{k}',
                foreground = "white",
                background = "black",
                width=w-1,
                heigh=h,
                borderwidth=5)
        b.bind('<ButtonPress>',play_sound(sounds[k])) # need to change from using external files -- row = 1, key = k
        # b.bind('<ButtonRelease>',release_key)
        b.grid(row=0, column=k, columnspan=2, sticky='n')
    return



window = tk.Tk()
window.title("very trashy interactive keyboard")

amp = 0.25
samp_sz = 16
samp_rt = 48000
f = 440
t = 1
wave = create_sine(amp,samp_sz,samp_rt,f,t)
waves = [wave] * 12

create_piano(window,waves)

window.mainloop()