### NEW GOAL:
#  	Input: ?
#	- An existing single-cycle waveform (maybe someday generate the waves internally)
#   Output: 64 wave files tuned in equal spacing -50 cents to +50 cents. For xfade loading into gotharman gear for 2-osc synthesis
#	- Make the two of the base pitch in the center
#   - Well what we really want is 48 collections of these 64 files, but that can be a wrapper or something.


import argparse, math, sys, os #, time, shutil,  sys, os, 
# from pathlib import Path

import sox


def main():
	parser = argparse.ArgumentParser(description='[]')
	parser.add_argument('-f', '--file', help='Input single-cycle waveform.')
	parser.add_argument('-o', '--outpath', help='The path to where the output folder will be created, where the frequency permutations will live')
	parser.add_argument('-s', '--speed_shift', default=1, type=int, help='Optional argument to add a speed offset to all generated detunes.')

	args = parser.parse_args()

	input_file_path = args.file
	output_path = args.outpath
	speed_shift = args.speed_shift

	if not (input_file_path and output_path):
		print("An input folder and output path must be specified. Exiting.")
		sys.exit(1)

	generate_detunes(input_file_path, output_path, speed_shift)

def generate_detunes(input_file_path, output_path, speed_shift=1):

	# So doubling the frequency is going up an octave. We want to go 1/24 up/down

	offset = 1/24

	adj_up_down = 31 #We do 31 

	speed_list_neg = [speed_shift-(x*(offset/adj_up_down)) for x in range(adj_up_down+1)]
	speed_list_pos = [speed_shift+(x*(offset/adj_up_down)) for x in range(adj_up_down+1)]
	speed_list = list(reversed(speed_list_neg)) + speed_list_pos #make it the full down to up

	print(speed_list)
	# print(len(speed_list))
	# print(str(1/24))

	if not os.path.exists(output_path):
		os.makedirs(output_path)

	base_speed = sox.file_info.sample_rate(input_file_path)
	# print(base_speed)

	# Loop generating permutations of the file, offsetting some number of cents on either side
	index = 1
	for speed in speed_list:
		print(speed) 
		trns = sox.Transformer()
		trns.rate(base_speed, quality='v') #supposedly setting "v" here increases the quality of the speed call below
		trns.speed(speed)
		trns.build_file(input_file_path, f"{output_path}/{index:03d}.wav")
		index += 1

if __name__ == "__main__":
	main()