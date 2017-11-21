#!/usr/bin/python

# Given a set of images and text, composite them together to create a video
# Copyright (C) 2017, Qatar Computing Research Institute, HBKU (author: Fahim Dalvi)
import argparse
import sys

from moviepy.editor import *

def main():
	parser = argparse.ArgumentParser(
		description='Simple movie clip creator',
		epilog='Sample Usage:  python simple_movie_creator.py --inputImages 1.jpg 2.jpg --inputText "hello" "second image" --output test.mp4')
	parser.add_argument('--inputImages', nargs='+', help='Space separated images to combine into a video', required=True)
	parser.add_argument('--inputText', nargs='+', help='Space separated titles for the images', required=True)
	parser.add_argument('--perImageDuration', type=int, help='Duration for each image in seconds', default=5)
	parser.add_argument('--output', help='filename of the output video', required=True)
	
	args = parser.parse_args()

	if (len(args.inputImages) != len(args.inputText)):
		print("Number of titles not equal to the number of images!")
		sys.exit(1)

	parts = []
	for image_idx, image in enumerate(args.inputImages):
		print("Compositing Image (%s) with Text (%s)"%(image, args.inputText[image_idx]))
		clip = ImageClip(image).set_duration(args.perImageDuration)

		# Generate a text clip. You can customize the font, color, etc.
		txt_clip = TextClip(args.inputText[image_idx],
			fontsize=30,
			color='white',
			bg_color='gray')

		# Say that you want it to appear 5s at the center of the screen
		txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(args.perImageDuration)
		parts.append(CompositeVideoClip([clip, txt_clip]))

	# Overlay the text clip on the first video clip
	video = concatenate_videoclips(parts, method="compose")

	# Write the result to a file (many options available !)
	video.write_videofile(args.output, fps=25)

if __name__ == '__main__':
	main()