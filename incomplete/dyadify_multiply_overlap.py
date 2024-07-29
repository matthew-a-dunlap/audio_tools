import argparse, math, sys #, time, shutil,  sys, os, 
# from pathlib import Path

import sox

# Input: Single-cycle waveform
# Output: Collection of single-cycle 

def main():
	parser = argparse.ArgumentParser(description='[]')
	parser.add_argument('-f', '--file', help='Input single-cycle waveform.')
	parser.add_argument('-o', '--outpath', help='The path to where the output folder will be created, where the dyad permutations will live')
	parser.add_argument('-c', '--concat', help='Wether the combined files should be concatenated together. An integer value is provided to define how many ms of gap should be between each sample (0 creates no gap).')

	args = parser.parse_args()

	input_file_path = args.file
	output_path = args.outpath

	if not (input_file_path and output_path):
	    print("An input folder and output path must be specified. Exiting.")
	    sys.exit(1)

	#Numerator, denominator. Approximations of equal temperment with max integer of 100. See https://pages.mtu.edu/~suits/RationalApprox.html
	ratios = [[1,1],[89,84],[55,49],[44,37],[63,50],[4,3],[99,70],[3,2],[100,63],[37,22],[98,55],[100,53],[2,1]]
	#keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	#levels = [1, .8, .6]

	# Open sample file
	# For each ratio:
	# - Create another version of the sample at the faster speed
	# - Calculate lowest common multiple (math.lcm) needed where the two speeds will line up seamlessly?
	#	- Wait I think I'm totally wrong, I just need to use the other half of the num/denom
	# - Extend two samples to be this length
	#	- ? How do I know how long to extend each one ?
	# - Place two samples ontop of each other (pydub?)

	#base_wave = AudioSegment.from_file(input_file_path, 'wav')


#TODO:  This works, but I actually want to chain together my combined files for the octave
#       I think I want to do 5 different level offsets for each of the 12 tones?
#		- I may do 5 levels of lower overtones, though that'll make tuning a bit more complicated
#			- Alternative is to do 2 levels of lower overtones and two of lower base notes
#	  	- Include the basic note as the first sample in the chain
#...
#	    When I generate these for real, I want to find lower octave single cycle waveforms

# Spazedrum allows you to import a folder of samples as chops. This is the way

# Gotta make outputs 16 bit 44.1
# Maybe force base sample to be 1024?
# - Transpose existing samples up an octave?
# - Or maybe just find samples that are this?

#{index}_({numerator}_{denominator}

	index = 0
	#for level in levels:
	for ratio in ratios:
		numerator = ratio[0]
		denominator = ratio[1]
		base_rate = sox.file_info.sample_rate(input_file_path)
		print(base_rate)

		b_trns = sox.Transformer()
		if denominator > 1:
			b_trns.repeat(denominator-1)
		b_trns.gain(gain_db=-6)
		base_output_path = f"{output_path}/base_{index}.wav"
		b_trns.build_file(input_file_path, f"{output_path}/base_{index}.wav")

		o_trns = sox.Transformer()
		print(numerator/denominator * base_rate)
#TODO: We should use rate instead to get the best quality, but I'm failing to get it to stay fast with a lower rate
		#o_trns.rate(numerator/denominator * base_rate, quality='v')
		o_trns.speed(numerator/denominator)
		if numerator > 1:	
			o_trns.repeat(numerator-1)
		o_trns.gain(gain_db=-6)
		#o_trns.set_output_format(rate=base_rate)
		#o_trns.convert(samplerate=base_rate)
		overtone_output_path = f"{output_path}/overtone_{index}.wav"
		o_trns.build_file(input_file_path, f"{output_path}/overtone_{index}.wav")

		c_trns = sox.Combiner()
		c_trns.convert(bitdepth=16)
		if args.concat is not None:
			concat_gap = int(args.concat)
			c_trns.pad(0,concat_gap/1000)

		c_trns.build([base_output_path, overtone_output_path], output_filepath=f"{output_path}/combined_{index}.wav", combine_type='mix')

		index += 1

	if args.concat is not None:
		concat_gap = int(args.concat)

		f_trns = sox.Combiner()
		input_array = [f"{output_path}/combined_{i}.wav" for i in range(index)]
		f_trns.build(input_array, output_filepath=f"{output_path}/full_combined.wav", combine_type='concatenate')

		#overtone_wave = base_wave._spawn(base_wave.raw_data, overrides={'frame_rate': overtone_rate}).set_frame_rate(44100)


		#combined_wave = (base_wave*denominator).overlay(overtone_wave*numerator)






		# Because combining waves has issues, we just output the two files of the same length
		# (base_wave*denominator).export(format='wav', out_f=f"{output_path}/base_{numerator}_{denominator}.wav")
		# (overtone_wave*numerator).export(format='wav', out_f=f"{output_path}/overtone_{numerator}_{denominator}.wav")

if __name__ == "__main__":
    main()