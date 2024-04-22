import numpy as np
import pygame


"""
Function: create and return a sine wave given parameters

Parameters:
1. freq: frequency in Hz of the sine wave

2. amp: amplitude of the sine wvae

3. duration: the duration in seconds of the sine wave

4. fs: sampling rate, set to a standard 44100 Hz

"""

def generate_sinwave(freq, amp, duration, fs = 44100):

     #generate time array
     t = np.linspace(0, duration, int(fs*duration), endpoint = False)

     #generate sine wave
     wave = amp * np.sin(2 * np.pi * freq * t)

     #helps smooth out sound at beginning and end
     window = np.hanning(len(t)) 
     wave *= window

     return wave

"""
Function: create a Sound object that can be used by the Pygame mixer (in this case a 16 bit PCM format)

Paramters: 
1. wave: the sin wave (or waves) to convert to the Pygame Sound object

Returns: Sound Object
"""

def create_pygame_sound(wave, fs = 44100):
    # Convert wave to 16-bit PCM format
    wave_pcm = np.int16(wave / np.max(np.abs(wave)) * 32767)

    # Convert mono to stereo by duplicating the channel
    stereo_wave = np.vstack((wave_pcm, wave_pcm)).T  # Transpose to get 2D array

    # Ensure the array is C-contiguous
    stereo_wave_contiguous = np.ascontiguousarray(stereo_wave)

    sound = pygame.sndarray.make_sound(stereo_wave_contiguous)
    return sound


"""
Function: to create and return a list of Psine waves in a pygame Sound Object format

Parameters:
1. duration = duration of the sine wave, in milliseconds
2. num_tones = number of sine wave tones to generate
3. freq_range = a list  of two values, where index 0 is the lowest frequency value for the sine wave
values, and index 1 is the highest possible frequency value for the sine wave
"""

    
def generator(duration, num_tones, freq_range):
    
    min_freq = freq_range[0]
    max_freq = freq_range[1]
    duration = duration / 1000

    sounds = []

    for _ in range(num_tones):
        rand_freq = np.random.uniform(min_freq, max_freq)
        wave = generate_sinwave(freq = rand_freq, amp = 1, duration = duration)
        sound = create_pygame_sound(wave)

        if sound:
            sounds.append(sound)

    
    return sounds

    



