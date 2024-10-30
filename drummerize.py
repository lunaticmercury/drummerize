#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:28:01 2024

@author: modestino
"""

import numpy as np
from scipy.io.wavfile import write

#note definition

class drum_generator:
    
    
    sample_rate = 44100
    
    note_frequencies = {
        'C1': 261.63,  # Do
        'C#1': 277.18,  # Do#
        'D1': 293.66,  # Re
        'D#1': 311.13,  # Re#
        'E1': 329.63,  # Mi
        'F1': 349.23,  # Fa
        'F#1': 369.99,  # Fa#
        'G1': 392.00,  # Sol
        'G#1': 415.30,  # Sol#
        'A1': 440.00,  # La
        'A#1': 466.16,  # La#
        'B1': 493.88,  # Si

        # Ottava superiore
        'C2': 523.25,  # Do
        'C#2': 554.37,  # Do#
        'D2': 587.33,  # Re
        'D#2': 622.25,  # Re#
        'E2': 659.25,  # Mi
        'F2': 698.46,  # Fa
        'F#2': 739.99,  # Fa#
        'G2': 783.99,  # Sol
        'G#2': 830.61,  # Sol#
        'A2': 880.00,  # La
        'A#2': 932.33,  # La#
        'B2': 987.77,  # Si
    }
    
    def __init__(self):
            super(drum_generator,self).__init__()


    def frequency_sweep(self,t, start_freq, end_freq):
            
        """
        Generates a frequency sweep signal that starts with a linear frequency variation 
        between a specified start and end frequency, then stabilizes at a constant frequency.
    
        Args:
            t (array-like): Time array representing the duration of the signal.\n
            start_freq (float): The starting frequency of the sweep.\n
            end_freq (float): The ending frequency of the sweep.\n
    
        Returns:
            np.ndarray: An array of frequencies with the first half as a variable frequency 
            sweep and the second half at a constant frequency.\n
        """
        
        # Crea la prima metà del segnale con una variazione lineare di frequenza
        freq_linear = np.linspace(start_freq, end_freq, int(len(t)/20))
        # Crea la seconda metà del segnale con frequenza costante
        freq_constant = np.linspace(end_freq, start_freq,len(t)-int(len(t)/20))
        # Concatena le due parti

        return np.concatenate([freq_linear, freq_constant])
    

    def create_adsr(self, duration, attack, decay, sustain, release):
        
        """
        Creates an ADSR (Attack, Decay, Sustain, Release) envelope based on specified durations for each phase.
        The envelope is used to shape the amplitude of a sound over time, controlling its progression from 
        initial attack to final release.
        
        Args:
            duration (float): Total duration of the envelope in seconds.\n
            attack (float): Duration of the attack phase in seconds.\n
            decay (float): Duration of the decay phase in seconds.\n
            sustain (float): Level of the sustain phase as a float between 0 and 1.\n
            release (float): Duration of the release phase in seconds.\n
        
        Returns:
            np.ndarray: An array representing the ADSR envelope with amplitude values.\n
        """
        
        sample_rate = self.sample_rate
        
        print("\n   /|\\ |     |")
        print("  / | \\|_____|")
        print(" /  |  |     |\\")
        print("/   |  |     | \\\n")
        print(" A    D   S     R")
        
        total_samples = int(sample_rate * duration)
        env = np.zeros(total_samples)
    
        # Calcola il numero di campioni per ciascuna fase
        attack_samples = int(sample_rate * attack)
        decay_samples = int(sample_rate * decay)
        release_samples = int(sample_rate * release)
        sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)
    
        # Controlla che sustain_samples sia positivo
        if sustain_samples < 0:
            raise ValueError("La durata totale non è sufficiente per il profilo ADSR specificato.")
    
        # Crea il profilo ADSR
        env[:attack_samples] = np.linspace(0, 1, attack_samples)  # Attack
        env[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain, decay_samples)  # Decay
        env[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain  # Sustain
        env[-release_samples:] = np.linspace(sustain, 0, release_samples)  # Release
        
        return env

    def kick(self,duration,A, D, S, R, base_freq, end_freq, noise_gain, gain,out_file):
        
        """
        Generates a synthesized kick drum sound by creating a frequency sweep and applying an ADSR envelope,
        noise, gain, and distortion effects. The sound is saved as a 16-bit WAV file.
        
        Args:
            duration (float): Total duration of the kick sound in seconds.\n
            A (float): Duration of the attack phase in seconds.\n
            D (float): Duration of the decay phase in seconds.\n
            S (float): Sustain level as a float between 0 and 1.\n
            R (float): Duration of the release phase in seconds.\n
            base_freq (float): Starting frequency of the frequency sweep in Hz.\n
            end_freq (float): Ending frequency of the frequency sweep in Hz.\n
            noise_gain (float): Amplitude of the noise component added to the kick sound.\n
            gain (float): Overall gain applied to the kick sound.\n
            out_file (str): Path where the generated sound will be saved as a WAV file.\n
        
        Returns:
            tuple: A tuple containing the time vector (t) and the generated kick waveform (kick_wave).\n
        """
        
        sample_rate = self.sample_rate
  
        # Time vector
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create the envelope generator
        adsr_env = self.create_adsr(duration, A, D, S, R)
            
        # Frequency sweep
        freq_env = self.frequency_sweep(t, base_freq ,end_freq)
        
        kick_wave = np.sin(2 * np.pi * freq_env * t) * adsr_env

        # Additive noise
        noise = 0.001*0.001*noise_gain*np.random.normal(0, len(t), len(t))  # Durata del rumore breve
        kick_wave += noise

        # Gain and distortion
        kick_wave = kick_wave * gain
        kick_wave = np.tanh(kick_wave)
        # Normalizzation and conversion in 16-bit
        kick_wave = np.clip(kick_wave * 32767, -32767, 32767).astype(np.int16)

        write(out_file, sample_rate, kick_wave)
        
        
        return  t, kick_wave
        
    def snare(self,duration,A, D, S, R, Amplitude, gain, out_file):
        
        """
         Generates a synthesized snare drum sound by creating a burst of noise shaped with an ADSR envelope.
         The sound is processed with gain and distortion, then saved as a 16-bit WAV file.
        
         Args:
             duration (float): Total duration of the snare sound in seconds.\n
             A (float): Duration of the attack phase in seconds.\n
             D (float): Duration of the decay phase in seconds.\n
             S (float): Sustain level as a float between 0 and 1.\n
             R (float): Duration of the release phase in seconds.\n
             Amplitude (float): Amplitude of the noise component for the snare sound.\n
             gain (float): Overall gain applied to the snare sound.\n
             out_file (str): Path where the generated snare sound will be saved as a WAV file.\n
        
         Returns:
             tuple: A tuple containing the time vector (t) and the generated snare waveform (snare_wave).\n
         """
         
        sample_rate = self.sample_rate
        
        # Time vector
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Create the envelope generator
        adsr_env = self.create_adsr(duration, A, D, S, R)
            
        # Aggiungi un breve burst di rumore per il "click" iniziale
        snare_wave =  0.01*Amplitude*np.random.normal(0, len(t), len(t))*adsr_env  # Durata del rumore breve

        # Gain and distortion
        snare_wave = snare_wave * gain
        snare_wave = np.tanh(snare_wave) 
        # Normalizzation and conversion in 16-bit
        snare_wave = np.clip(snare_wave * 32767, -32767, 32767).astype(np.int16)

        write(out_file, sample_rate, snare_wave)
        
        return t, snare_wave
            
    def sine(self, note, out_file = None):
        
        """
        Generates a sine wave tone for a specified note. Optionally saves the generated tone to a 16-bit WAV file.
        
        Args:
            note (str): The note to generate (e.g., 'A4'), which is used to look up the frequency in `note_frequencies`.\n
            out_file (str, optional): Path where the generated sine wave will be saved as a WAV file.\n
        
        Returns:
            np.ndarray: An array containing the sine wave samples.\n
        """

        sample_rate = self.sample_rate
        
        Amplitude   = 0.8
        duration    = 0.1
        
        # Time vector
        t = np.linspace(0, duration, int(sample_rate * duration))
            
     
        sine =  Amplitude * np.sin(2 * np.pi * self.note_frequencies[note] * t)   # Durata del rumore breve

        sine = np.tanh(sine) 
        # Normalizzation and conversion in 16-bit
        sine.astype(np.int16)

        if (out_file !=  None):
            write(out_file, sample_rate, sine)
        
        return sine

    def silent(self, duration, out_file = None):
        
        """
        Generates a silent audio signal (array of zeros) for a specified duration. 
        Optionally saves the silent signal as a WAV file.
        
        Args:
            duration (float): Duration of the silent audio in seconds.\n
            out_file (str, optional): Path where the silent audio will be saved as a WAV file.\n
        
        Returns:
            np.ndarray: An array containing the silent audio samples (zeros).\n
        """
        
        sample_rate = self.sample_rate
        

        # Aggiungi un breve burst di rumore per il "click" iniziale
        silent = 0*np.ones(int(sample_rate * duration))   # Durata del rumore breve

        if (out_file !=  None):
            write(out_file, sample_rate, silent)
        
        return silent
    
    def mixer(self,  ch1_vol,ch2_vol,ch3_vol, ch1, ch2 = None,  ch3 = None, out_file = None):
        
        """
        Mixes up to three audio channels with specified volume levels for each. 
        The resulting mix can optionally be saved to a 16-bit WAV file.
        
        Args:
            ch1_vol (float): Volume for channel 1, ranging from 0 to 1.
            ch2_vol (float): Volume for channel 2, ranging from 0 to 1.
            ch3_vol (float): Volume for channel 3, ranging from 0 to 1.
            ch1 (np.ndarray): The first audio channel.
            ch2 (np.ndarray, optional): The second audio channel, default is None.
            ch3 (np.ndarray, optional): The third audio channel, default is None.
            out_file (str, optional): Path where the mixed audio will be saved as a WAV file.
        
        Returns:
            np.ndarray: An array containing the mixed audio samples.
        """
        
        sample_rate = self.sample_rate
        
        
        #conditions
        
        if(ch2_vol == 0 and  ch3_vol == 0):
            
            input_sample = ch1 * ch1_vol
            
        if(ch2_vol != 0 and  ch3_vol == 0):
            
            input_sample = ch1 * ch1_vol/2 + ch2 * ch2_vol/2
        
        if(ch2_vol != 0 and  ch3_vol != 0):
                
                input_sample = ch1 * ch1_vol/3 + ch2 * ch2_vol/3 + ch3 * ch3_vol/3
            
            
        
        if (out_file !=  None):
            
            write(out_file, sample_rate, input_sample)
            
        
        return input_sample