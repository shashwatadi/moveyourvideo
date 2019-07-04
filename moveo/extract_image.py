import cv2 
import numpy as np
import csv
import os
import subprocess
import shutil
import ffmpeg

import cvlib as cv
from cvlib.object_detection import draw_bbox

  
from os.path import isfile, join

def FrameCapture(video_file_path, params): 

	vidObj = cv2.VideoCapture(video_file_path)
	########################################################
	input = ffmpeg.input(video_file_path)
	audio = input.audio
	# video = input.video
	# print(type(video))
	# out = ffmpeg.output(audio, video, 'out.mp4')
	########################################################

	fps = vidObj.get(cv2.CAP_PROP_FPS)
	print("FPS : {}".format(fps))

	audio_path = "audio.mp3"
	if os.path.exists(audio_path):
		os.remove(audio_path)

	# get audio from video file
	# command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(video_file_path, audio_path)
	# FNULL = open(os.devnull, 'w')
	# subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

	# Used as counter variable 
	count = -1
	num_params = np.shape(params)[0]
	print(num_params)
	for param in params:
		param[0]=int(param[0]*fps)
		param[1]=int(param[1]*fps)
	i=0

	success, image = vidObj.read()

	center_y = int((image.shape[0]/2)*0.975)	
	height = int((image.shape[0]/2)*0.875)
	width = int(height*4/5)
	center_x = width+300
	print(image.shape)
	size = (width*2,height*2)

	pathOut = "/home/atman/work/moviecrop/result.mp4"
	if os.path.exists(pathOut):
		os.remove(pathOut)
	out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps/2, size)
	# success=0
	while success:

		count += 1
		success, image = vidObj.read()
		if(count%2!=0):
			continue
		if(success!=1):
			print("break here : {}".format(count))
			break


		if(i<num_params and count>params[i][1]):
			i += 1

		if(i<num_params and count>params[i][0] and count<params[i][1]):
			if(width < center_x+params[i][2] < image.shape[1] - width):
				center_x += int(params[i][2])
			if(height < center_y+params[i][3] < image.shape[0] - height):	
				center_y += int(params[i][3])

		if(count%100==0):
			print(count)
		image = image[center_y-height:center_y+height,center_x-width:center_x+width]
		if(count%30==0):
			bbox, label, conf = cv.detect_common_objects(image)
		image = draw_bbox(image, bbox, label, conf)
		out.write(image)

	print("Video ban gya")
	out.release()

	print("\nFRAMES CREATED\n")

	if os.path.exists("FINAL1.mp4"):
		os.remove("FINAL1.mp4")

	#add audio
	# command = "ffmpeg -i {} -i Kaisehua2.mp3 -c copy -map 0:v -map 1:a FINAL1.mp4".format(pathOut)
	# subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
	input = ffmpeg.input(pathOut)
	video = input.video
	out = ffmpeg.output(audio, video, 'FINAL.mp4')
	print("saved video")
	ffmpeg.run(out)

# Driver Code 
if __name__ == '__main__': 
  
	# Calling the function

	with open('/home/atman/work/moviecrop/parameters.csv', 'r') as f:
	    reader = csv.reader(f)
	    params = list(reader)
	params = [[float(i) for i in row] for row in params ]
	print("read the parameters")
	video_file_path = "/home/atman/work/moviecrop/input_video.mp4"
	FrameCapture(video_file_path, params) 

























#convertovideo
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    print("Converting frames to videos ")
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
    filename=pathIn + files[0]
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)

    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        # print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        out.write(img)
        #inserting the frames into an image array
        # frame_array.append(img)

    # for i in range(len(frame_array)):
    #     # writing to a image array
    #     out.write(frame_array[i])
    print("Video ban gya")
    out.release()