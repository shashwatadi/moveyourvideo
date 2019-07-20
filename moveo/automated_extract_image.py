import cv2 
import numpy as np
import csv
import os
import subprocess
import shutil
import ffmpeg

import urllib.request


import cvlib as cv
from cvlib.object_detection import draw_bbox

  
from os.path import isfile, join

def FrameCapture(video_file_path): 

	vidObj = cv2.VideoCapture("https://moveovideo.s3.ap-south-1.amazonaws.com/56496159_443708599714226_5667207495941095424_n.mp4")
	success, image = vidObj.read()
	print("\nsuccess = {}\n".format(success))

	print(type(vidObj))
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
	
	success, image = vidObj.read()
	print("success = {}".format(success))
	center_y = int((image.shape[0]/2)*0.975)	#526
	height = int((image.shape[0]/2)*0.875)  #472
	width = int(height*4/5)		#377
	center_x = width+300	#677	
	print(image.shape)
	size = (width*2,height*2)

	pathOut = "/home/atman/work/moviecrop/result.mp4"
	if os.path.exists(pathOut):
		os.remove(pathOut)
	out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
	# success=0
	max_x = image.shape[1] - width
	max_y = image.shape[0] - height
	speed_x = 0
	speed_y = 0
	print("max_x:{}".format(max_x))
	print("max_y:{}".format(max_y))
	while success:

		count += 1
		success, image = vidObj.read()
		# if(count%2!=0):
		# 	continue
		if(success!=1):
			print("break here : {}".format(count))
			break

		if(count%30==0):
			bbox, label, conf = cv.detect_common_objects(image)
			# print(bbox)
			if bbox:
				print(bbox)
				x1 = bbox[0][0]
				x2 = bbox[0][2]
				y1 = bbox[0][1]
				y2 = bbox[0][3]
				X = x1+x2
				left = 2*(center_x-width/6)
				right = 2*(center_x+width/6)
				Y = y1+y2
				top = 2*(center_y+height/10)
				bottom = 2*(center_y-height/10)
				print("x1+x2={}  left={}  right={}".format(X,left,right))
				print("y1+y2={}  top={}  bottom={}".format(Y,top,bottom))
				if(X<left):
					speed_x = -2
				elif(X>right):
					speed_x = 2
				else:
					speed_x = 0

				if(Y<bottom):
					speed_y = -2
				elif(Y>top):
					speed_y = 2
				else :
					speed_y = 0

			
		if(center_x>width and center_x<max_x):
			center_x += speed_x
			print("count : {} | center_x : {} | speed_x : {} | width : {}".format(count, center_x, speed_x,width))
		if(center_y+speed_y>height and center_y+speed_y<max_y):
			center_y += speed_y
			print("count : {} | center_y : {} | speed_y : {} | height : {}".format(count, center_y, speed_y, height))
			# print("center_x = {} and center_y = {}".format(center_x, center_y))
		image = draw_bbox(image, bbox, label, conf)
		image = image[center_y-height:center_y+height,center_x-width:center_x+width]
		out.write(image)

	print("Video ban gya")
	out.release()

	print("\nFRAMES CREATED\n")

	if os.path.exists("FINAL.mp4"):
		os.remove("FINAL.mp4")

	#add audio
	# command = "ffmpeg -i {} -i Kaisehua2.mp3 -c copy -map 0:v -map 1:a FINAL1.mp4".format(pathOut)
	# subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
	input = ffmpeg.input(pathOut)
	video = input.video
	out = ffmpeg.output(audio, video, 'FINAL1.mp4')
	print("saved video")
	ffmpeg.run(out)

# Driver Code 
if __name__ == '__main__': 
  
	# Calling the function

	# with open('/home/atman/work/moviecrop/parameters.csv', 'r') as f:
	#     reader = csv.reader(f)
	#     params = list(reader)
	# params = [[float(i) for i in row] for row in params ]
	# print("read the parameters")

	with urllib.request.urlopen("https://moveovideo.s3.ap-south-1.amazonaws.com/56496159_443708599714226_5667207495941095424_n.mp4") as url:
		s = url.read()
		# I'm guessing this would output the html source code ?
		print(type(s))


	video_file_path = "https://moveovideo.s3.ap-south-1.amazonaws.com/56496159_443708599714226_5667207495941095424_n.mp4" #"https://moveovideo.s3.ap-south-1.amazonaws.com/input_video.mp4"  #"/home/atman/work/moviecrop/input_video.mp4"
	FrameCapture(video_file_path) 