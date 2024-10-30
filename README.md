# Drum Sound Generator

This project provides a `drum_generator` class for synthesizing basic drum and percussion sounds, including kick and snare drums, sine tones, and silent segments, as well as tools for mixing audio channels. Each sound can be generated with customizable parameters and saved as a WAV file for use in audio applications.

## Features

- **Kick Drum Synthesis**: Creates kick drum sounds using frequency sweeps and ADSR envelopes.
- **Snare Drum Synthesis**: Generates snare drum sounds using noise bursts shaped with ADSR envelopes.
- **Sine Tone Generation**: Synthesizes sine tones for specified musical notes.
- **Silent Sound Generation**: Produces silent audio signals of specified durations.
- **Mixer**: Combines up to three audio channels with specified volume levels.
- **Frequency Sweep**: Creates frequency sweeps that can be used for sound design.

## Requirements

- **Python 3.x**
- **NumPy**
- **SciPy**

To install dependencies, run:
```bash
pip install numpy scipy
```

## Usage

To use the drum_generator class, first import it and create an instance:
```python
from drummerize import drum_generator

drum_gen = drum_generator()
```
