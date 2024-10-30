#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 22:09:31 2024

@author: Modestino Carbone

"""

from drummerize import drum_generator
import numpy as np

drum = drum_generator()

# kick generation

duration = 0.1    # Durata totale

attack = 0.02    # Durata dell'attacco
decay = 0.04    # Durata del decay
sustain = 0.08    # Livello di sustain
release = 0.01    # Durata del release

gain = 3.0
n_gain = 0.02

t, kick_wave = drum.kick(duration, attack, decay, 
                         sustain, release, 50, 300, 
                         n_gain, gain, "kick.wav")

# snare generation

Amplitude = 0.01
gain = 1

attack = 0.03    # Durata dell'attacco
decay = 0.03    # Durata del decay
sustain = 0.2     # Livello di sustain
release = 0.01    # Durata del release

t, snare_wave = drum.snare(duration, attack, decay, 
                           sustain, release, 
                           Amplitude, gain, "snare.wav")


# note enveloper

adsr_env = drum.create_adsr(duration, attack, decay, sustain, release)


# seqence generation

drum.mixer(1, 0, 0,

           ch1=np.concatenate(

               (drum.sine('C1')*adsr_env,
                drum.silent(0.1),
                drum.sine('A1')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('E1')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('A1')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('F2')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('G1')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('E1')*adsr_env,
                   drum.silent(0.1),
                   drum.sine('A2')*adsr_env,
                   drum.silent(0.1))),
           out_file="sequence.wav"

           )


# chords

cmajor = drum.mixer(1, 1, 1, ch1=drum.sine('C1')*adsr_env,
                    ch2=drum.sine('E1')*adsr_env,
                    ch3=drum.sine('G1')*adsr_env)

cmajor_mod = drum.mixer(1, 1, 1, ch1=drum.sine('C1')*adsr_env,
                        ch2=drum.sine('E1')*adsr_env,
                        ch3=drum.sine('B1')*adsr_env)

fmajor = drum.mixer(1, 1, 1, ch1=drum.sine('F1')*adsr_env,
                    ch2=drum.sine('A1')*adsr_env,
                    ch3=drum.sine('C1')*adsr_env)

# chord progression example 1

immagine = np.concatenate(

    (cmajor,
     drum.silent(0.7),
     cmajor,
     drum.silent(0.7),
     cmajor,
     drum.silent(0.7),
     cmajor_mod,
     drum.silent(0.7),
     fmajor,
     drum.silent(0.7),
     fmajor,
     drum.silent(0.7),
     fmajor,
     drum.silent(0.7),
     drum.sine('A1')*adsr_env,
     drum.silent(0.1),
     drum.sine('A#1')*adsr_env,
     drum.silent(0.1),
     drum.sine('B1')*adsr_env)

)


drum.mixer(1, 0, 0, immagine, out_file="progression.wav")
