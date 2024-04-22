import numpy as np
import random
import pygame

"""
Function: create a Sound object that can be used by the Pygame mixer (in this case a 16 bit PCM format)

Paramters: 
1. wave: the sin wave (or waves) to convert to the Pygame Sound object

Returns: Sound Object
"""


def create_pygame_sound(wave):
    # Convert wave to 16-bit PCM format
    wave_pcm = np.int16(wave / np.max(np.abs(wave)) * 32767)

    # Convert mono to stereo by duplicating the channel
    stereo_wave = np.vstack((wave_pcm, wave_pcm)).T  # Transpose to get 2D array

    # Ensure the array is C-contiguous
    stereo_wave_contiguous = np.ascontiguousarray(stereo_wave)

    sound = pygame.sndarray.make_sound(stereo_wave_contiguous)

    return sound

"""
Function: Adjust a frequency using a given number of cents

Parameters:
1. freq: the base freq, in Hz
2. cents: the number of cents to adjust the frequency by

Returns: adjusted frequency in Hz

"""

def adjust_frequency(freq, cents):

    factor = 2 ** (abs(cents) / 1200)
    return freq * factor if cents >=0 else freq / factor


"""
Function: to create an evenly distributed tone cloud around a base frequnecy with varying octaves

Parameters:
1. numClouds: the number of clouds to generate

2. numDevianets: how many deviants from the target freq to include in the tone cloud

3. duration: the length of each cloud in seconds

4. target_freq: middle octave target frequency

5. octave_variance: how much octave varaince we want. If low, only want three octaves (1 below and above target freq).
                         if high, want five octaves (2 below and 2 above target freq)

Returns: plays the actual sound using Pygame Mixer, and returns the sin wave array that was played

"""

def toneCloud(numClouds, numDeviants, duration, target_freq, octave_variance):

    # Set up basic, constant attributes for the tones
    Fs = 44100
    Ts = 1/Fs
    T = 0.075
    t = np.arange(0, T, Ts)
    window = np.hanning(len(t))

    #Create a list of freq at different octaves give variance
    
    if octave_variance =="high" or octave_variance == "low":
        oct1 = target_freq / 4
        oct2 = target_freq / 2
        oct3 = target_freq 
        oct4 = target_freq * 2
        oct5 = target_freq * 4

        octave_freq = [oct1, oct2, oct3, oct4, oct5]



    #silence for stable ton
    Tsilence = 0.258333333 # 333ms - 75 ms to achieve a 3Hz rate

    #attributes for cloud stim timing
    cloudBegin = 0.5 #offset (in seconds) from the standard tones
    cloudDensity = 50 #number of distractor tones per second

    for a in range(numClouds): #creating 

        # Set up ranges for the clouds
        cloudHigh_min = target_freq * 1.5 #min value for the highest freq 
        cloudHigh_max = target_freq * 5 #max value for the higheset freq 
        cloudLow_min = target_freq * 0.20 #min value for lowest freq
        cloudLow_max = target_freq * 0.75 #max value for lowest freq

        # Generate random frequencies for high and low ranges

        #calculates the number of high frequencies 
        #assuming half the cloudDensity will be high tone 
        #therefore, mulitply by duration to get number of high freq tones, accounting for 0.5 second offset

        num_high = np.round((duration - 0.5) * (cloudDensity / 2)).astype(int) 
        num_low = num_high  # Assuming same number of high and low frequency waves for tone cloud 

        #generate random arrays for both low and high frequencies, rounded to the nearest integer
        cloudHigh_array = np.round(np.random.uniform(cloudHigh_min, cloudHigh_max, num_high)) 
        cloudLow_array = np.round(np.random.uniform(cloudLow_min, cloudLow_max, num_low))

        # Combine and shuffle the frequencies
        cloudFinal_array = np.concatenate([cloudHigh_array, cloudLow_array])
        np.random.shuffle(cloudFinal_array)

    # Initialize silence and sound arrays
    cloudSilence = np.zeros(int(np.round(Fs * cloudBegin)) - 1) #calculates the number of silent values, and insert 0s into these posiitons
    cloudSound = np.zeros(int(duration * Fs)) #these 0s serve as placeholders for sound entries

    # Main loop
    for i, freq in enumerate(cloudFinal_array): #iterating over array with high and low frequency waves

        #for the first tone (i == 0), i is set to 0
        #calculate the starting index for the tone
        startPoint = int(np.round(Fs * (1 / cloudDensity) * (i - 1))) if i > 0 else 0

        #generates the individual tone (sine wave)
        yC = np.sin(2 * np.pi * freq * t)
        yC *= window #smooths the start and end of tone

        tempVec = np.zeros(startPoint) #create a temporary array of 0s with length of startPoint
        tempVec = np.concatenate([tempVec, yC]) #concatenates the temporary array of silence with the generated tone

        endPad = np.zeros(len(cloudSound) - len(tempVec)) #creates an endpad array of 0s to smooth out tone
        tempVec = np.concatenate([tempVec, endPad]) #adds this endpad array to the temporary array

    cloudSound += tempVec #add the complete tone array (with padded silence) to the Sound array

    # Combine silence and sound
    cloudSoundFinal = np.concatenate([cloudSilence, cloudSound]) #combine sound and silent arrays

    totalTargets = int(duration * 3) #calculate number of deviant tones based on 3Hz and duration (3*duration)
    targetDeviants = np.zeros(totalTargets) #initializes an array of 0s with length of totalTargets

    # Generate deviant locations
    #randomly selects deviant locations, ensuring deviants are not at very beginning or very end
    deviantLoc = np.round(np.random.uniform(1, totalTargets - 1, numDeviants)).astype(int) 

    # Ensure deviants are separated
    #if devaints are within three locations of one another, recalculate deviant locations and check locations again
    while numDeviants > 1 and (np.max(deviantLoc) - np.min(deviantLoc)) < 3: 
        deviantLoc = np.round(np.random.uniform(1, totalTargets - 1, numDeviants)).astype(int)

    # Mark deviant locations by changing Deviant array at said index to 1, rather than 0
    for i in range(totalTargets):
        targetDeviants[i] = 1 if i in deviantLoc else 0

    # Generate tones
    targetY = np.array([]) #empty array to store tones

    for is_deviant in targetDeviants:

        target_freq = random.choice(octave_freq)

        #if tone is not deviant, generate tone using target frequency


        if is_deviant == 0:
            Y = np.sin(2 * np.pi * target_freq * t) * window 

        #if tone is deviant, pitch shift the target frequency (by *1.122462)    
        else: #add in cents here to shift value
            

            # Define the range of cents for adjustment
            max_cents = 10 #range of -25 to 25

            # Randomly choose to increase or decrease the frequency
            cents_change = random.randint(-max_cents, max_cents)

            new_freq = adjust_frequency(target_freq, cents_change)

            Y = np.sin(2 * np.pi * (new_freq) * t) * window

        Y0 = np.zeros(int(np.round(Fs * Tsilence)))#adds silence after each tone
        Ys = np.concatenate([Y, Y0]) #combines tone with silence array
        targetY = np.concatenate([targetY, Ys]) #combine all tones together

    # Create ramp for fade-out at end of the sound
    cloudRamp = np.concatenate([
        np.ones(int(Fs * (duration - 0.1))), #creates an array of 1s
        np.linspace(1, 0, int(Fs * 0.1)) #adds inearly decreasing numbers from 1 to 0 over the last 100 ms
    ])

    # Apply fade-out to the tone cloud
    cloudSoundFinal = cloudSoundFinal[:len(targetY)] #trims silence array to the length of tone array
    cloudSoundFinal *= cloudRamp #applies ramp fade out to silence array


    # Reformat sound array
    sound_output = create_pygame_sound(wave = targetY)

    #play sound
    sound_output.play()

    # Keep the program running until the sound finishes
    pygame.time.wait(int(duration * 1000))

    return targetY

"""
Function: to play a number of tone clouds in a row. This allows the tone clouds to be played while the Alien is moving

Parameters: 
1. numClouds: number of clouds to play

2. duration: duration (in seconds) of each cloud

3. freq: middle base freq

4. is_target_callable: allows repeated checking of a break condition. Allows the code to terminate tone clouds early if Alien
reached target. ***Do not change in game.py

5. octave_variance: whether we want low octave variance (3 octaves) or high octave variance (5 octaves)

"""

def play_repeated_tone(numClouds, duration, freq, is_target_callable, octave_variance):

        for _ in range(numClouds):

            if is_target_callable(): #if we want to continue playing
                break
            tone = toneCloud(1, 10, duration, freq, octave_variance)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    y = toneCloud(1, 0, 3, 293.66, "low")





    

