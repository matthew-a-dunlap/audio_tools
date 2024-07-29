# audio_tools
This repository contains tools useful for manipulating audio files, specifically intended for use with Gotharman audio machines (Little Deformer 3 etc).

# Impetus
This code was created because the Gotharman LD3 only has one synthesized oscillator per part, which can make it a challenge to create certain sounds (detuned oscillator phasing, dyads, etc). I found a workaround by using the xfad sampler mode, which allows you to loop two audio files at once. Long story short, you can use the two xfad layers at standalone oscillators with their own detuning!

# Files

If you provide `detunes_across_octaves.py` a single-cycle waveform (or any audio file) it will provide you back a folder of wav files. Each wav file is actually 64 single-cycle waveforms detuned from -.5 to .5 semitones. These can be loaded onto an LD3 xfad oscillator, and then the chop/chop2 parameters can be used to control detuning of the two oscillators. Furthermore you can generated multiple octaves of detuned chop collections, and load the intervals you want to be playing out of your "oscillator".

`folder_to_wav_with_cues.py` is a child script called to generate octaves of detunes, but can be called directly. It will turn a folder of wav files into a single wav file. Most importantly, it uses wav file cue points which are supported by Gotharman gear. This means if you load the wav all the chops will be already present without any work. This works around a limitation with the LD3, where loading a folder of wavs as chops adds dead air to the end of each chop meaning you cannot loop them seamlessly.

`generate_detunes.py` can also be called directly if you want to generate 64 detunes across -.5 to .5 semitones for a provided wav.
