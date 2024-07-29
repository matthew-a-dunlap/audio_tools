### Input: a folder of wave files
### Output: a single wave file with the cue points for the wave file embedded

# This is to allow importing usable loop packs to Gotharman synths, as the built in functionality adds empty space after each cue.

import os
import wave
import argparse
import struct
from wavelibrary import Wave

def main():
    parser = argparse.ArgumentParser(description='Concatenate WAV files with cue points')
    parser.add_argument('-i','--input_folder', help='Path to the folder containing WAV files')
    parser.add_argument('-o','--output_file', help='Path to the output concatenated WAV file')
    args = parser.parse_args()

    concatenate_wav_files_with_cue_points(args.input_folder, args.output_file)

def concatenate_wav_files_with_cue_points(input_folder, output_file):

    # Check if the output file ends with '.wav'
    if not output_file.lower().endswith('.wav'):
        output_file += '.wav'

    # List all files in the input folder
    files = os.listdir(input_folder)
    
    # Initialize variables for wave file parameters
    output_wave = None
    output_params = None
    cue_points = []

    try:
        for file_name in files:
            if file_name.lower().endswith('.wav'):
                file_path = os.path.join(input_folder, file_name)
                
                # Open the current wave file
                with wave.open(file_path, 'rb') as wave_file:
                    # Read parameters from the first file
                    if output_wave is None:
                        output_wave = wave.open(output_file, 'wb')
                        output_params = wave_file.getparams()
                        output_wave.setparams(output_params)
                    
                    # Read and write audio frames
                    frames = wave_file.readframes(wave_file.getnframes())
                    output_wave.writeframes(frames)
                    
                    cue_points.append(output_wave.getnframes())

    finally:
        if output_wave is not None:
            output_wave.close()

    output_wave = Wave(output_file)
    output_wave.write(output_file, markers=cue_points)


    print(f"Concatenated {len(files)} wave files into {output_file} with cue points")

if __name__ == "__main__":
    main()