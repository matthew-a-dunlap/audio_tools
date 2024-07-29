import argparse, sys, os, shutil

from generate_detunes import generate_detunes
from folder_to_wav_with_cues import concatenate_wav_files_with_cue_points

def main():
	parser = argparse.ArgumentParser(description='[Call generate_detunes and folder_to_wav_with_cues to generate a folder of ordered chop wavs across a specified range]')
	parser.add_argument('-f', '--file', help='Input single-cycle waveform.')
	parser.add_argument('-n', '--file_note', help='The note of the input file, used to label outputs.')
	parser.add_argument('-o', '--outpath', help='The path to where the output folder will be created, where our pitched files of frequency permutations will live')
	parser.add_argument('-b', '--bottom_octave', type=int, help='Integer specifying the lowest octave of our generated range')
	parser.add_argument('-t', '--top_octave', type=int, help='Integer specifying the highest octave of our generated range')

	args = parser.parse_args()

	input_file_path = args.file
	output_path = args.outpath
	bottom_octave = args.bottom_octave 
	top_octave = args.top_octave 
	file_note = args.file_note

	if not (input_file_path and output_path):
		print("An input file and output path must be specified. Exiting.")
		sys.exit(1)

	if not (bottom_octave is not None and top_octave is not None):
		print("An bottom and top octave must be specified. Exiting.")
		sys.exit(1)

	semitone_mult = pow(2, 1/12) #about 1.05946309436
	pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', "B"]
	pitch_name_start = pitch_names.index(file_note)
	print(pitch_name_start)

	# print(list(range(bottom_octave*12, top_octave*12)))
	# print(list(range(-12,0)))

	#folders = []

	pn_counter = 0 #pitch name counter
	for semi in range(bottom_octave*12, top_octave*12):
		speed = 1
		if semi < 0:
			for _ in range(semi,0):
				speed = speed / semitone_mult
		else:
			for _ in range(semi):
				speed = speed * semitone_mult

		print(str(speed))
		full_path_dt = os.path.join(output_path, 'detunes', f'dt{semi}')
		generate_detunes(input_file_path, full_path_dt, speed)
		out_file_name = f'w{bottom_octave + pn_counter//12}{pitch_names[pn_counter%12]}.wav'
		concatenate_wav_files_with_cue_points(full_path_dt, os.path.join(output_path, out_file_name))
		pn_counter += 1

	shutil.rmtree(os.path.join(output_path, 'detunes'))
		#folders.append(sub_path)


		#I need to clean up my generated detunes at the end

	#print(str(semitone_mult))

	# So, it looks like sox doesn't have an inbuilt way to adjust by speed by semitone, only pitch
	# I need a formula for that
	# maybe: https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/

	# TODO:
	# Here call generate_detunes and folder_to_wav_with_cues across a range

if __name__ == "__main__":
	main()